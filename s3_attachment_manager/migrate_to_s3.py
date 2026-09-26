import logging
import os
import shutil
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("s3_migration")

def migrate_attachments_to_s3(env, limit=10, batch_size=50, last_id=0, backup_dir="/home/odoo/filestore_backup"):
    """
    Migra los archivos adjuntos almacenados localmente en el filestore hacia S3/MinIO.
    
    :param env: Entorno de Odoo.
    :param limit: Número máximo de registros a consultar en este bloque.
    :param batch_size: Frecuencia de commits a la BD.
    :param last_id: Filtrar registros con ID mayor a last_id para evitar atascos con archivos omitidos/faltantes.
    :param backup_dir: Ruta de respaldo para mover los archivos migrados.
    """
    Attachment = env['ir.attachment']
    domain = [
        ('store_fname', '!=', False),
        ('id', '>', last_id),
        ('url', '=', False),
        ('mimetype', 'not in', ['text/css', 'application/javascript', 'text/javascript'])
    ]
    
    # Obtener credenciales de S3
    s3_bucket, s3_access_key_id, s3_secret_access_key, s3_endpoint_url = Attachment._get_s3_credentials()
    client_kwargs = {
        "aws_access_key_id": s3_access_key_id,
        "aws_secret_access_key": s3_secret_access_key,
    }
    if s3_endpoint_url:
        client_kwargs["endpoint_url"] = s3_endpoint_url

    s3_client = boto3.client("s3", **client_kwargs)

    attachments = Attachment.search(domain, order='id asc', limit=limit)
    total_count = Attachment.search_count(domain)
    
    to_process = len(attachments)
    _logger.info(f"=== INICIANDO MIGRACIÓN ===")
    _logger.info(f"Total de adjuntos pendientes en BD (ID > {last_id}): {total_count}")
    _logger.info(f"Adjuntos a procesar en este lote: {to_process}")
    
    if not attachments:
        _logger.info("No hay adjuntos para procesar con los criterios dados.")
        return last_id

    success_count = 0
    skipped_count = 0
    error_count = 0
    bytes_transferred = 0
    max_processed_id = last_id

    for idx, attachment in enumerate(attachments, 1):
        max_processed_id = attachment.id
        fname = attachment.store_fname
        
        try:
            full_path = Attachment._full_path(fname)
            
            # 1. Verificar si ya existe en S3
            already_in_s3 = False
            try:
                s3_client.head_object(Bucket=s3_bucket, Key=fname)
                already_in_s3 = True
            except ClientError:
                already_in_s3 = False

            if already_in_s3:
                # Si ya está en S3 pero el archivo todavía existe localmente, moverlo al backup para liberar espacio local
                if os.path.exists(full_path):
                    if backup_dir:
                        dest_path = os.path.join(backup_dir, env.cr.dbname, fname)
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.move(full_path, dest_path)
                    _logger.info(f"[{idx}/{to_process}] ID {attachment.id}: Archivo '{fname}' ya estaba en S3. Copia local movida a backup.")
                else:
                    _logger.info(f"[{idx}/{to_process}] ID {attachment.id}: Archivo '{fname}' ya existe en S3. Omitiendo.")
                skipped_count += 1
                continue

            # 2. Si no está en S3, verificar si existe en el filestore local
            if not os.path.exists(full_path):
                _logger.warning(f"[{idx}/{to_process}] ID {attachment.id}: Archivo local no encontrado en {full_path}. Omitiendo.")
                skipped_count += 1
                continue
            
            file_size = os.path.getsize(full_path)
            
            with open(full_path, 'rb') as f:
                bin_data = f.read()
            
            # 3. Subir a S3
            res = Attachment._store_file_write(fname, bin_data)
            
            if res:
                bytes_transferred += file_size
                mb_transferred = bytes_transferred / (1024 * 1024)
                _logger.info(f"[{idx}/{to_process}] ID {attachment.id} ({file_size / 1024:.1f} KB): Subido a S3. Total lote: {mb_transferred:.2f} MB")
                
                # Mover a carpeta de respaldo garantizando su creación
                if backup_dir:
                    dest_path = os.path.join(backup_dir, env.cr.dbname, fname)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.move(full_path, dest_path)
                
                success_count += 1
            else:
                _logger.error(f"[{idx}/{to_process}] ID {attachment.id}: Falló la subida a S3.")
                error_count += 1
                
        except Exception as e:
            _logger.exception(f"[{idx}/{to_process}] ID {attachment.id}: Error en archivo '{fname}': {e}")
            error_count += 1
            
        if idx % batch_size == 0:
            env.cr.commit()
            _logger.info(f"--- Commit BD guardado ({idx}/{to_process}) ---")

    env.cr.commit()
    _logger.info(f"=== RESUMEN LOTE ===")
    _logger.info(f"Exitosos: {success_count} | Omitidos: {skipped_count} | Errores: {error_count}")
    _logger.info(f"Total datos migrados: {bytes_transferred / (1024 * 1024):.2f} MB")
    _logger.info(f"Último ID procesado en este lote: {max_processed_id}")
    
    return max_processed_id

if __name__ == '__main__':
    migrate_attachments_to_s3(env)



