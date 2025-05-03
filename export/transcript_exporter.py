"""
Módulo para exportar transcripciones a diferentes formatos.
"""
import json
import csv
import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Union

class TranscriptExporter:
    """
    Clase para manejar la exportación de transcripciones a diferentes formatos.
    """
    
    def __init__(self, export_dir: str = "exports"):
        """
        Inicializa el exportador con un directorio para guardar las exportaciones.
        
        Args:
            export_dir: Directorio donde se guardarán los archivos exportados
        """
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)
        
    def _generate_filename(self, base_name: Optional[str] = None, extension: str = "txt") -> str:
        """
        Genera un nombre de archivo único para la exportación.
        
        Args:
            base_name: Nombre base para el archivo (opcional)
            extension: Extensión del archivo
            
        Returns:
            Nombre de archivo único
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        
        if base_name:
            filename = f"{base_name}_{timestamp}_{unique_id}.{extension}"
        else:
            filename = f"transcript_{timestamp}_{unique_id}.{extension}"
            
        return filename
    
    def export_as_text(self, transcript: str, filename: Optional[str] = None) -> str:
        """
        Exporta la transcripción como archivo de texto plano.
        
        Args:
            transcript: Texto de la transcripción
            filename: Nombre de archivo personalizado (opcional)
            
        Returns:
            Ruta al archivo exportado
        """
        if not filename:
            filename = self._generate_filename(extension="txt")
            
        file_path = self.export_dir / filename
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(transcript)
            
        return str(file_path)
    
    def export_as_json(self, transcript: str, metadata: Optional[Dict] = None, 
                      filename: Optional[str] = None) -> str:
        """
        Exporta la transcripción como archivo JSON con metadatos adicionales.
        
        Args:
            transcript: Texto de la transcripción
            metadata: Diccionario con metadatos adicionales
            filename: Nombre de archivo personalizado (opcional)
            
        Returns:
            Ruta al archivo exportado
        """
        if not filename:
            filename = self._generate_filename(extension="json")
            
        file_path = self.export_dir / filename
        
        data = {
            "transcript": transcript,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        return str(file_path)
    
    def export_as_csv(self, transcript: str, metadata: Optional[Dict] = None,
                     filename: Optional[str] = None) -> str:
        """
        Exporta la transcripción como archivo CSV.
        
        Args:
            transcript: Texto de la transcripción
            metadata: Diccionario con metadatos adicionales
            filename: Nombre de archivo personalizado (opcional)
            
        Returns:
            Ruta al archivo exportado
        """
        if not filename:
            filename = self._generate_filename(extension="csv")
            
        file_path = self.export_dir / filename
        
        # Preparar datos para CSV
        header = ["timestamp", "transcript"]
        row = [datetime.now().isoformat(), transcript]
        
        # Añadir metadatos si existen
        if metadata:
            for key, value in metadata.items():
                header.append(key)
                row.append(str(value))
        
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(row)
            
        return str(file_path)
    
    def prepare_for_ai(self, transcript: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Prepara la transcripción para ser enviada a un modelo de IA.
        
        Args:
            transcript: Texto de la transcripción
            metadata: Metadatos adicionales (opcional)
            
        Returns:
            Diccionario con datos formateados para la IA
        """
        ai_ready_data = {
            "transcript": transcript,
            "source": "voice_query",
            "timestamp": datetime.now().isoformat(),
            "processing_stage": "transcription_complete"
        }
        
        if metadata:
            ai_ready_data["metadata"] = metadata
            
        return ai_ready_data 