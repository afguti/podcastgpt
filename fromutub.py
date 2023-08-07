
#credit to https://python.langchain.com/docs/integrations/document_loaders/youtube_audio
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

def vidcontent(url: str, num=0) -> list:
    if not(os.path.exists(f'./youtube{num}/')):
        save_dir = f"./youtube{num}"
        loader = GenericLoader(YoutubeAudioLoader([url], save_dir), OpenAIWhisperParser())
        docs = loader.load()
        file_path = os.path.join(f"./youtube{num}", 'docs.txt')
        with open(f"./youtube{num}/docs.txt", "w") as file:
            for item in docs:
                file.write(str(item) + "\n")
    else:
        print(f"Folder ./youtube{num} exist.")
        docs = []
        with open(f"./youtube{num}/docs.txt", "r") as file:
            for line in file:
                line = line.strip()
                docs.append(line)
    while True:
        q = input("Your query: ")
        resp = queryvid(docs, q)
        print(resp)

def queryvid(docs: list, q: str) -> str:
    # Combine doc
    combined_docs = [doc.page_content for doc in docs]
    text = " ".join(combined_docs)
    # Split them
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    splits = text_splitter.split_text(text)
    # Build an index
    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.from_texts(splits, embeddings)
    # Build a QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=0),
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
    )
    return qa_chain.run(q)

