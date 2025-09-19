# Project Plan: Arcane Scribe

**Project Goal:** To create a distributable, cross-platform desktop application that allows users to query RPG rulebooks (PDFs) using natural language. The solution will run entirely locally, provide answers with source citations, and be licensed as Free and Open-Source Software (FOSS).

**Core Technologies:**

- **Language:** Python
    
- **AI Architecture:** Retrieval-Augmented Generation (RAG)
    
- **LLM:** Google Gemma (GGUF format)
    
- **LLM Runner:** `llama-cpp-python`
    
- **Vector DB:** ChromaDB
    
- **UI Framework:** CustomTkinter
    
- **Packaging:** PyInstaller
    

## **Timeline Overview**

|Phase|Weeks|Estimated End Date|Key Outcome|
|---|---|---|---|
|**Phase 1: Core Engine Development**|3|Oct 9, 2025|A functional command-line RAG tool.|
|**Phase 2: Application & UI Development**|3|Oct 30, 2025|A feature-complete graphical application.|
|**Phase 3: Packaging & Distribution**|1|Nov 6, 2025|A publicly released v1.0 executable.|
|**Phase 4: Post-Release & Maintenance**|Ongoing|-|Community support and future development.|

## **Phase 1: Core Engine Development (The "Headless" Version)**

_(Estimated Duration: 3 Weeks | Target End: October 9, 2025)_

**Goal:** Build and validate the entire RAG pipeline as a command-line tool. This ensures the core logic is solid before building the UI.

### **Week 1: Setup & PDF Processing**

- [x] **Task 1.1:** Initialize Git repository and set up the Python project environment (`venv`).
    
- [x] **Task 1.2:** Write the PDF ingestion script to process all `.pdf` files in a user-specified directory.
    
- [x] **Task 1.3:** Integrate `pypdf` for text extraction and metadata capture (filename, page number).
    
- [x] **Task 1.4:** Implement text chunking logic to split extracted text into meaningful, overlapping segments.
    
- [x] **Task 1.5:** Integrate a Sentence-Transformers model (e.g., `bge-small-en-v1.5`) to convert text chunks into vector embeddings.
    
- [x] **Task 1.6:** Set up an embedded ChromaDB instance to store the chunks, embeddings, and source metadata.
    
- **Milestone 1 (Achieved Sep 19, 2025):** A script that can successfully process a folder of PDFs and save them into a local, persistent vector database.
    

### **Week 2: RAG Query & Generation**

- [ ] **Task 2.1:** Implement the query function: take a user's question, embed it using the same model.
    
- [ ] **Task 2.2:** Perform a similarity search against ChromaDB to retrieve the most relevant text chunks.
    
- [ ] **Task 2.3:** Integrate `llama-cpp-python` to load and run a quantized Gemma model (GGUF).
    
- [ ] **Task 2.4:** Develop a robust prompt template that instructs the model to answer based _only_ on the provided context and to cite sources.
    
- [ ] **Task 2.5:** Generate an answer from the LLM and parse its output.
    
- **Milestone 2:** A command-line tool that accepts a question and returns a well-formatted, cited answer based on the indexed PDFs.
    

### **Week 3: Advanced Logic & Refinement**

- [ ] **Task 3.1:** Implement the logic for handling rule-combination queries (e.g., "How do Grapple and Shove work together?").
    
- [ ] **Task 3.2:** Use the LLM in a preliminary step to decompose the complex query into individual topics ("Grapple", "Shove").
    
- [ ] **Task 3.3:** Implement multi-query retrieval to fetch context for all decomposed topics.
    
- [ ] **Task 3.4:** Create a "synthesis prompt" that asks the LLM to explain each rule individually and then describe their interaction.
    
- [ ] **Task 3.5:** Write basic unit tests for the core components (chunking, data storage) to ensure stability.
    
- **Milestone 3:** The command-line tool can now accurately answer both simple and complex rule-combination questions.
    

## **Phase 2: Application & UI Development**

_(Estimated Duration: 3 Weeks | Target End: October 30, 2025)_

**Goal:** Wrap the core engine in a user-friendly and intuitive graphical interface.

### **Week 4: UI Scaffolding & Model Management**

- [ ] **Task 4.1:** Set up a CustomTkinter project structure.
    
- [ ] **Task 4.2:** Design and implement the main window layout: a pane for managing PDF sources, a central chat/results window, and a status bar.
    
- [ ] **Task 4.3:** Implement the "first-run" setup logic to create a dedicated folder for models and databases.
    
- [ ] **Task 4.4:** Build the automatic model downloader (for Gemma and the embedding model) with a progress bar to provide feedback to the user.
    
- **Milestone 4:** The application starts, checks for models, downloads them if necessary, and displays a functional main window.
    

### **Week 5: Integrating Core Logic with UI**

- [ ] **Task 5.1:** Connect the UI to the PDF processing engine. Users should be able to select a directory and see indexing progress.
    
- [ ] **Task 5.2:** Implement the chat input field and the results display area.
    
- [ ] **Task 5.3:** Connect the user's query to the RAG engine. **Crucially, run the AI processing in a separate thread to prevent the UI from freezing.**
    
- [ ] **Task 5.4:** Display the LLM's response in the results area, formatting it for readability (e.g., using markdown).
    
- **Milestone 5:** The application is fully interactive. A user can manage PDFs, ask questions, and receive cited answers through the GUI.
    

### **Week 6: Polishing & User Experience (UX)**

- [ ] **Task 6.1:** Add an application icon.
    
- [ ] **Task 6.2:** Implement robust error handling (e.g., "Invalid PDF," "Model download failed") and display user-friendly messages.
    
- [ ] **Task 6.3:** Add quality-of-life features: "Clear Chat," "Copy Answer," and a loading indicator while the LLM is thinking.
    
- [ ] **Task 6.4:** Ensure the UI resizes gracefully and looks good on different screen resolutions.
    
- [ ] **Task 6.5:** Conduct basic user testing to identify and fix obvious usability issues.
    
- **Milestone 6:** The application is feature-complete, stable, and provides a polished user experience.
    

## **Phase 3: Packaging & Distribution**

_(Estimated Duration: 1 Week | Target End: November 6, 2025)_

**Goal:** Create a standalone, distributable executable and prepare for a public F/OSS release.

### **Week 7: Build, Test, and Document**

- [ ] **Task 7.1:** Create and configure a PyInstaller build script (`.spec` file) to bundle all necessary assets and data files.
    
- [ ] **Task 7.2:** Generate executables for target platforms (Windows, macOS, Linux).
    
- [ ] **Task 7.3:** Test the executables on clean virtual machines to ensure they run without any external dependencies.
    
- [ ] **Task 7.4:** Write a comprehensive `README.md` file detailing the project's purpose, features, how to use it, and how to contribute.
    
- [ ] **Task 7.5:** Choose and add a `LICENSE` file (e.g., MIT or Apache 2.0).
    
- [ ] **Task 7.6:** Include the Gemma Terms of Use file in the distribution package.
    
- [ ] **Task 7.7:** Create a v1.0 release on GitHub, uploading the executables as release assets.
    
- **Milestone 7:** Version 1.0 of Arcane Scribe is publicly available on GitHub.
    

## **Phase 4: Post-Release & Future Features**

_(Ongoing)_

**Goal:** Support the community and plan the future of the project.

- [ ] **Ongoing:** Monitor GitHub Issues for bug reports and feature requests.
    
- [ ] **Ongoing:** Engage with users and provide support.
    
- [ ] **v1.1 Plan:** Address initial feedback and bug fixes.
    
- [ ] **Stretch Goal:** Add support for other document formats (`.txt`, `.md`).
    
- [ ] **Stretch Goal:** Explore a more advanced UI using a framework like Tauri for a potential v2.0.