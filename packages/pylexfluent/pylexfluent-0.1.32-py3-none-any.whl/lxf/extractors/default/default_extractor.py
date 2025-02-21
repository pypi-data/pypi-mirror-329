#######################################
import os
import logging
from lxf.settings import get_logging_level

logger = logging.getLogger('default extractor')
fh = logging.FileHandler('./logs/default_extractor.log')
fh.setLevel(get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(get_logging_level())
logger.addHandler(fh)
########################################


from lxf.ai.text_analysis.default_text_analysis import  lemmatize_and_extract_entities, segment_text_into_chunks, summarize_chunks
from lxf.services.try_safe import try_safe_execute_async
from lxf.domain.extracted_data import HIERARCHIE_DOCUMENT, HIERARCHIE_DOSSIER, Chunk, ChunkMetadata, ExtractedData, ExtractedMetadata

# def default_chunks_extractor(full_file_path:str,**kwargs)->tuple[str,dict] :
#     logger.debug("Aucune donnee extraite depuis l'extracteur par defaut!")
#     return f'Defaut Extractor',None

def default_chunks_extractor(text: str,**kwargs) -> ExtractedData|None:
    """
    Effectue la segmentation et la reconnaissance d'entités nommées sur un texte donné.
    """    
    try:    
        if text == None :
            logging.error("Le texte fourni est vide")
            return None
        chunks = segment_text_into_chunks(text)
        source="fichier.ext"
        if chunks == None: 
            logging.error("Aucun chunk genere apres la segmentation.")
            return  None
        extracted_data = ExtractedData()
        extracted_data.metadata=ExtractedMetadata()
        extracted_data.chunks=[]
        nb:int = len(chunks) +1
        # chunking des extraits de texte
        for i, chunk_text in enumerate(chunks):
            chunk = Chunk()
            chunk.metadata = ChunkMetadata()
            chunk.metadata.chunk=i + 1
            chunk.metadata.chunks=nb
            chunk.metadata.title=f"Extrait"        
            chunk.metadata.source=source        
            chunk.metadata.hierarchie = HIERARCHIE_DOCUMENT
            chunk.page_content = chunk_text #lemmatized_text  
            chunk.metadata.description = f"Extrait n° {i+1}"
            extracted_data.chunks.append(chunk)

        # Ajout du résumé 
        chunk_summaries = summarize_chunks(text) 
        global_summary = " ".join(chunk_summaries)  
        chunk = Chunk()
        chunk.metadata = ChunkMetadata()
        chunk.metadata.chunk = nb
        chunk.metadata.chunks = nb
        chunk.metadata.hierarchie = HIERARCHIE_DOSSIER        
        chunk.metadata.source =source    
        chunk.metadata.title="Résumé"
        chunk.metadata.description="Résumé du document"
        chunk.page_content=global_summary
        extracted_data.chunks.append(chunk)

    except Exception as e:
            logging.error(f"Erreur lors de la generation du resume global pour {source}.\nException : {e}")
            return None
    return extracted_data





##### Sementic splitting 
    #         volume_name = extract_volume_name(object_key) or bucket
    #         name_collection = volume_name

    #         store = get_vectors_store(collection_name=name_collection, url=url, port=port, apikey=api_key, embeddings=embeddings)

    #         ext = full_file_path.rpartition(".")[-1].strip().upper()
    #         loader = None

    #         if ext == PDF:
    #             loader = PyPDFLoader(full_file_path)
    #         elif ext in [DOC, DOCX]:
    #             loader = Docx2txtLoader(full_file_path)
    #         else:
    #             loader = UnstructuredFileLoader(full_file_path)

    #         documents: List[Document] = loader.load()
    #         text = "".join([sanitize_text(doc.page_content) for doc in documents])

    #         segments = segment_text_into_chunks(text)
    #         nbr_segments = len(segments)
    #         document_name = os.path.basename(object_key)
    #         new_docs: List[Document] = []
    #         for segment in segments:
    #             metadata = {
    #                 'source': object_key,
    #                 'ext': ext,
    #                 'bucket': bucket,
    #                 'nombre de chunks': nbr_segments,
    #                 'tags': {'volume_name': volume_name, 'document_name': document_name}
    #             }
    #             new_doc = Document(page_content=segment, metadata=metadata)
    #             new_docs.append(new_doc)

    #         store.add_documents(new_docs)
    #         logger.debug(f"Documents ajoutés avec succès dans la collection {name_collection}.")

    #     result = update_job_status(unit_of_work.indexation_repository(), job_to_update.id, "completed")
    #     if result:
    #         check_and_delete_file_if_jobs_completed(unit_of_work.job_repository(), parent_id, full_file_path)
    #     else:
    #         logger.warning(f"Premier essai de mise à jour du statut pour Id {job_id} a échoué.")
    #         time.sleep(0.3)
    #         result = update_job_status(unit_of_work.indexation_repository(), job_to_update.id, "completed")
    #         if result:
    #             check_and_delete_file_if_jobs_completed(unit_of_work.job_repository(), parent_id, full_file_path)
    #         else:
    #             logger.error(f"Second essai de mise à jour du statut pour Id {job_id} a échoué.")

    # except Exception as ex:
    #     logger.exception(f"Une erreur s'est produite lors de l'ajout du fichier à la collection : {ex}")