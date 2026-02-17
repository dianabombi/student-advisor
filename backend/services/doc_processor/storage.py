"""
MinIO Storage Service

Enhanced storage service with multi-bucket support for document management.
"""

import os
import logging
from typing import Optional, List, Dict
from datetime import timedelta
from minio import Minio
from minio.error import S3Error
from io import BytesIO
from pathlib import Path

logger = logging.getLogger(__name__)


class MinIOStorage:
    """
    Enhanced MinIO storage service with multi-bucket support.
    
    Buckets:
    - raw-docs: Original uploaded documents
    - processed-docs: OCR'd and processed documents
    - templates: Document templates
    - filled-docs: Filled template documents
    
    Features:
    - Multi-bucket management
    - Upload/download files
    - Generate presigned URLs
    - File versioning
    - Metadata management
    """
    
    # Bucket names
    BUCKET_RAW = "raw-docs"
    BUCKET_PROCESSED = "processed-docs"
    BUCKET_TEMPLATES = "templates"
    BUCKET_FILLED = "filled-docs"
    
    def __init__(
        self,
        endpoint: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        secure: bool = False
    ):
        """
        Initialize MinIO client with multi-bucket support.
        
        Args:
            endpoint: MinIO endpoint (default from env)
            access_key: Access key (default from env)
            secret_key: Secret key (default from env)
            secure: Use HTTPS (default: False)
        """
        self.endpoint = endpoint or os.getenv('MINIO_ENDPOINT', 'minio:9000')
        self.access_key = access_key or os.getenv('MINIO_ROOT_USER', 'minioadmin')
        self.secret_key = secret_key or os.getenv('MINIO_ROOT_PASSWORD', 'minioadmin')
        self.secure = secure
        
        # Initialize MinIO client
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )
        
        # Ensure all buckets exist
        self._ensure_buckets()
        
        logger.info(f"MinIO initialized: {self.endpoint}")
    
    def _ensure_buckets(self):
        """Create all required buckets if they don't exist."""
        buckets = [
            self.BUCKET_RAW,
            self.BUCKET_PROCESSED,
            self.BUCKET_TEMPLATES,
            self.BUCKET_FILLED
        ]
        
        for bucket in buckets:
            try:
                if not self.client.bucket_exists(bucket):
                    self.client.make_bucket(bucket)
                    logger.info(f"Created bucket: {bucket}")
            except S3Error as e:
                logger.error(f"Error ensuring bucket {bucket}: {e}")
    
    def upload_raw_document(
        self,
        file_data: bytes,
        filename: str,
        user_id: Optional[int] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Upload raw document to raw-docs bucket.
        
        Args:
            file_data: File content as bytes
            filename: Original filename
            user_id: User ID (for organization)
            metadata: Additional metadata
            
        Returns:
            Object name in MinIO
        """
        # Generate object name with user prefix
        if user_id:
            object_name = f"user_{user_id}/{filename}"
        else:
            object_name = filename
        
        # Prepare metadata
        file_metadata = metadata or {}
        file_metadata['original_filename'] = filename
        
        # Upload to raw-docs bucket
        return self._upload_file(
            self.BUCKET_RAW,
            file_data,
            object_name,
            metadata=file_metadata
        )
    
    def upload_processed_document(
        self,
        file_data: bytes,
        filename: str,
        original_object_name: str,
        processing_info: Optional[Dict] = None
    ) -> str:
        """
        Upload processed document to processed-docs bucket.
        
        Args:
            file_data: Processed file content
            filename: Filename for processed document
            original_object_name: Reference to original document
            processing_info: Processing metadata
            
        Returns:
            Object name in MinIO
        """
        # Prepare metadata
        metadata = processing_info or {}
        metadata['original_document'] = original_object_name
        metadata['processed_filename'] = filename
        
        # Upload to processed-docs bucket
        return self._upload_file(
            self.BUCKET_PROCESSED,
            file_data,
            filename,
            metadata=metadata
        )
    
    def upload_template(
        self,
        file_data: bytes,
        template_name: str,
        template_type: str = "contract"
    ) -> str:
        """
        Upload document template to templates bucket.
        
        Args:
            file_data: Template file content
            template_name: Template name
            template_type: Type of template
            
        Returns:
            Object name in MinIO
        """
        object_name = f"{template_type}/{template_name}"
        
        metadata = {
            'template_type': template_type,
            'template_name': template_name
        }
        
        return self._upload_file(
            self.BUCKET_TEMPLATES,
            file_data,
            object_name,
            metadata=metadata
        )
    
    def upload_filled_document(
        self,
        file_data: bytes,
        filename: str,
        template_name: str,
        source_document: Optional[str] = None
    ) -> str:
        """
        Upload filled document to filled-docs bucket.
        
        Args:
            file_data: Filled document content
            filename: Output filename
            template_name: Template used
            source_document: Source document reference
            
        Returns:
            Object name in MinIO
        """
        metadata = {
            'template_used': template_name,
            'filled_filename': filename
        }
        
        if source_document:
            metadata['source_document'] = source_document
        
        return self._upload_file(
            self.BUCKET_FILLED,
            file_data,
            filename,
            metadata=metadata
        )
    
    def _upload_file(
        self,
        bucket: str,
        file_data: bytes,
        object_name: str,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Internal method to upload file to specified bucket.
        
        Args:
            bucket: Bucket name
            file_data: File content
            object_name: Object name
            content_type: MIME type
            metadata: File metadata
            
        Returns:
            Object name
        """
        try:
            file_stream = BytesIO(file_data)
            file_size = len(file_data)
            
            # Detect content type from filename if not provided
            if content_type == "application/octet-stream":
                content_type = self._get_content_type(object_name)
            
            self.client.put_object(
                bucket,
                object_name,
                file_stream,
                file_size,
                content_type=content_type,
                metadata=metadata
            )
            
            logger.info(f"Uploaded to {bucket}/{object_name} ({file_size} bytes)")
            return object_name
        
        except S3Error as e:
            logger.error(f"Error uploading file: {e}")
            raise
    
    def download_file(self, bucket: str, object_name: str) -> bytes:
        """
        Download file from specified bucket.
        
        Args:
            bucket: Bucket name
            object_name: Object name
            
        Returns:
            File content as bytes
        """
        try:
            response = self.client.get_object(bucket, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            
            logger.info(f"Downloaded {bucket}/{object_name} ({len(data)} bytes)")
            return data
        
        except S3Error as e:
            logger.error(f"Error downloading file: {e}")
            raise
    
    def download_raw_document(self, object_name: str) -> bytes:
        """Download from raw-docs bucket."""
        return self.download_file(self.BUCKET_RAW, object_name)
    
    def download_processed_document(self, object_name: str) -> bytes:
        """Download from processed-docs bucket."""
        return self.download_file(self.BUCKET_PROCESSED, object_name)
    
    def download_template(self, template_name: str) -> bytes:
        """Download from templates bucket."""
        return self.download_file(self.BUCKET_TEMPLATES, template_name)
    
    def get_presigned_url(
        self,
        bucket: str,
        object_name: str,
        expires: timedelta = timedelta(hours=1)
    ) -> str:
        """
        Generate presigned URL for temporary file access.
        
        Args:
            bucket: Bucket name
            object_name: Object name
            expires: URL expiration time
            
        Returns:
            Presigned URL
        """
        try:
            url = self.client.presigned_get_object(
                bucket,
                object_name,
                expires=expires
            )
            
            logger.info(f"Generated presigned URL for {bucket}/{object_name}")
            return url
        
        except S3Error as e:
            logger.error(f"Error generating presigned URL: {e}")
            raise
    
    def get_raw_document_url(self, object_name: str, expires: timedelta = timedelta(hours=1)) -> str:
        """Get presigned URL for raw document."""
        return self.get_presigned_url(self.BUCKET_RAW, object_name, expires)
    
    def get_processed_document_url(self, object_name: str, expires: timedelta = timedelta(hours=1)) -> str:
        """Get presigned URL for processed document."""
        return self.get_presigned_url(self.BUCKET_PROCESSED, object_name, expires)
    
    def delete_file(self, bucket: str, object_name: str):
        """
        Delete file from specified bucket.
        
        Args:
            bucket: Bucket name
            object_name: Object name
        """
        try:
            self.client.remove_object(bucket, object_name)
            logger.info(f"Deleted {bucket}/{object_name}")
        
        except S3Error as e:
            logger.error(f"Error deleting file: {e}")
            raise
    
    def list_files(self, bucket: str, prefix: str = "", recursive: bool = True) -> List[Dict]:
        """
        List files in bucket with metadata.
        
        Args:
            bucket: Bucket name
            prefix: Filter by prefix
            recursive: List recursively
            
        Returns:
            List of file information dictionaries
        """
        try:
            objects = self.client.list_objects(
                bucket,
                prefix=prefix,
                recursive=recursive
            )
            
            files = []
            for obj in objects:
                files.append({
                    'name': obj.object_name,
                    'size': obj.size,
                    'last_modified': obj.last_modified,
                    'etag': obj.etag
                })
            
            logger.info(f"Listed {len(files)} files in {bucket} with prefix: {prefix}")
            return files
        
        except S3Error as e:
            logger.error(f"Error listing files: {e}")
            raise
    
    def list_user_documents(self, user_id: int, bucket: str = None) -> List[Dict]:
        """
        List all documents for a specific user.
        
        Args:
            user_id: User ID
            bucket: Specific bucket (default: raw-docs)
            
        Returns:
            List of user's documents
        """
        bucket = bucket or self.BUCKET_RAW
        prefix = f"user_{user_id}/"
        return self.list_files(bucket, prefix)
    
    def file_exists(self, bucket: str, object_name: str) -> bool:
        """
        Check if file exists in bucket.
        
        Args:
            bucket: Bucket name
            object_name: Object name
            
        Returns:
            True if exists, False otherwise
        """
        try:
            self.client.stat_object(bucket, object_name)
            return True
        except S3Error:
            return False
    
    def get_file_metadata(self, bucket: str, object_name: str) -> Dict:
        """
        Get file metadata.
        
        Args:
            bucket: Bucket name
            object_name: Object name
            
        Returns:
            File metadata dictionary
        """
        try:
            stat = self.client.stat_object(bucket, object_name)
            return {
                'size': stat.size,
                'last_modified': stat.last_modified,
                'etag': stat.etag,
                'content_type': stat.content_type,
                'metadata': stat.metadata
            }
        except S3Error as e:
            logger.error(f"Error getting metadata: {e}")
            raise
    
    def _get_content_type(self, filename: str) -> str:
        """
        Determine content type from filename.
        
        Args:
            filename: Filename
            
        Returns:
            MIME type
        """
        ext = Path(filename).suffix.lower()
        
        content_types = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.doc': 'application/msword',
            '.txt': 'text/plain',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.tiff': 'image/tiff'
        }
        
        return content_types.get(ext, 'application/octet-stream')

