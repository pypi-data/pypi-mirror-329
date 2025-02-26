Below is a **comprehensive set of rules** for the `MarkdownChunkingStrategy` class, meticulously designed to handle the intricacies of Markdown document structures. These rules encompass **chunk size management**, **content type preservation**, **structural integrity**, **duplicate prevention**, and **automatic detection of headers and footers**. Additionally, they incorporate your specific requirements regarding **hard length limits**, **table splitting with full headers**, and **automatic identification of repeating headers and footers**.

# Rules
---

## **1. Chunk Size Management**

### **1.1. Minimum Length (`min_chunk_len`)**
- **Definition:** The minimum number of characters a chunk must contain.
- **Default:** `512`
- **Rule:** 
  - Ensure each chunk is at least `min_chunk_len` characters long.
  - Merge smaller chunks with adjacent ones to meet this requirement.

### **1.2. Soft Maximum Length (`soft_max_len`)**
- **Definition:** The preferred upper limit for chunk size.
- **Default:** `1024`
- **Rule:** 
  - Aim to keep chunks below `soft_max_len`.
  - Allow slight exceedances if necessary to preserve structural elements.

### **1.3. Hard Maximum Length (`hard_max_len`)**
- **Definition:** The absolute maximum number of characters a chunk can contain.
- **Default:** `2048`
- **Rule:** 
  - Strictly enforce that no chunk exceeds `hard_max_len`.
  - If a chunk exceeds this limit, split it at logical boundaries (e.g., sentence endings, newlines) regardless of content type.

---

## **2. Content Type Preservation**

### **2.1. Headings**
- **Identification:** Detect headings using various Markdown syntaxes (e.g., `#`, `##`, numbered headings).
- **Rules:** 
  - Preserve all heading levels and formats.
  - When splitting, ensure that headings remain intact and appropriately formatted within chunks.
  - **Heading-Based Chunking:** 
    - Headings should be the primary points for chunk decisions.
    - Contents belonging to a heading should remain in the same chunk as the heading whenever possible.
    - No chunk should end with a heading or with only a small amount of content after a heading.
    - When a chunk must be split, prefer splitting between sections (at heading boundaries).
    - Ensure a heading's content stays cohesive by keeping as much of a section together as possible.

### **2.2. Tables**
- **Identification:** Detect Markdown tables by the presence of pipe characters (`|`) and separator lines (e.g., `---`).
- **Rules:** 
  - **No Split Rule:** Do not split tables across chunks unless they exceed `hard_max_len`.
  - **Splitting with Full Headers:** If a table must be split due to the hard length limit, ensure that each resulting chunk includes the full table header to maintain clarity and structure.

### **2.3. Footnotes and Citations**
- **Identification:** Detect footnote definitions (e.g., `[^1]: Footnote text`) and citations (e.g., `[@citation]`).
- **Rules:** 
  - Keep footnote markers and their corresponding definitions within the same chunk.
  - Avoid splitting footnote definitions across multiple chunks.

### **2.4. Images and Links**
- **Identification:** Detect Markdown image syntax (`![Alt Text](url)`) and links (`[Text](url)`).
- **Rules:** 
  - Ensure that images and links are not split across chunks.
  - Maintain the integrity of image and link syntax within chunks.
  - **Cross-Chunk References:** Enhance handling of links that point between chunks by tracking link targets and their containing chunks.

### **2.5. Code Blocks and Inline Code**
- **Identification:** Detect fenced code blocks (e.g., ```` ```python ````) and inline code (e.g., `` `code` ``).
- **Rules:** 
  - **Code Blocks:** Never split within a fenced code block. Include both opening and closing fences within the same chunk.
  - **Inline Code:** Avoid splitting inline code snippets across chunks. Ensure that both backticks are within the same chunk.

### **2.6. Lists**
- **Identification:** Detect ordered (`1.`, `2.`, ...) and unordered lists (`-`, `*`, `+`).
- **Rules:** 
  - Do not split lists across chunks.
  - Preserve list hierarchies and indentation levels.
  - If a list exceeds `hard_max_len`, consider splitting between major sections or logical breaks, ensuring individual list items remain intact.

### **2.7. Blockquotes**
- **Identification:** Detect blockquotes using the `>` symbol.
- **Rules:** 
  - Keep entire blockquotes within the same chunk.
  - Preserve nesting and indentation within blockquotes.

### **2.8. Embedded HTML**
- **Identification:** Detect embedded HTML tags within the Markdown.
- **Rules:** 
  - Do not split embedded HTML elements across chunks.
  - Ensure that opening and closing HTML tags are contained within the same chunk.

### **2.9. Tables of Contents (TOC)**
- **Identification:** Detect TOCs, typically represented as nested lists with links to headings.
- **Rules:** 
  - Optionally exclude TOCs from chunking or place them in a separate chunk.
  - Ensure that TOC links correspond to headings within the same or subsequent chunks.

### **2.10. YAML Front Matter**
- **Identification:** Detect YAML front matter enclosed within `---` at the beginning of the document.
- **Rules:** 
  - Keep YAML front matter intact within a single chunk, preferably the first chunk.
  - Do not split YAML front matter across multiple chunks.

### **2.11. Emphasis and Formatting**
- **Identification:** Detect bold (`**bold**`), italics (`*italics*`), strikethrough (`~~text~~`), and other formatting.
- **Rules:** 
  - Avoid splitting emphasis markers across chunks.
  - Ensure that formatting syntax remains intact within chunks.

### **2.12. Horizontal Rules and Page Breaks**
- **Identification:** Detect horizontal rules (`---`, `***`, `___`) and page breaks.
- **Rules:** 
  - Preserve horizontal rules and page breaks within the same chunk.
  - Use them as natural split points for chunking.

---

## **3. Logical Split Points**

### **3.1. Natural Language Boundaries**
- **Rule:** 
  - Prefer splitting at sentence endings (e.g., `.` followed by a space) or newline characters (`\n`) to maintain readability and coherence.

### **3.2. Exclusion of Key Elements**
- **Rule:** 
  - Do not split within structural elements such as tables, code blocks, lists, blockquotes, images, links, and embedded HTML to preserve their functionality and appearance.

---

## **4. Markdown Integrity**

### **4.1. Consistent Formatting**
- **Rule:** 
  - Ensure that all Markdown syntax within each chunk is correctly formatted.
  - Maintain proper heading levels, list structures, and other formatting conventions.

### **4.2. Content Type Classification**
- **Rule:** 
  - Classify blocks of text (e.g., paragraphs, tables, headings) to apply appropriate formatting and prevent structural issues post-chunking.

---

## **5. Duplicate Prevention**

### **5.1. Exact Duplicates**
- **Rule:** 
  - Utilize hashing (e.g., MD5) to identify and exclude exact duplicate content blocks, ensuring each chunk contains unique information.

### **5.2. Fuzzy Duplicates**
- **Rule:** 
  - Implement fuzzy duplicate detection using similarity metrics (e.g., Levenshtein distance) to identify and manage near-duplicate content.
  - Set a configurable threshold for similarity to determine when content should be considered a duplicate.
  - Preserve the most comprehensive version of similar content blocks.

---

## **6. Header and Footer Management**

### **6.1. Advanced Identification of Headers and Footers**
- **Rule:** 
  - Implement sophisticated pattern recognition to detect repeating headers and footers without relying on predefined templates.
  - Use machine learning techniques or advanced heuristics to identify patterns across document sections.
  - Consider contextual information beyond exact matches to detect variant headers/footers.
  - Use heuristics such as consistent phrases, patterns (e.g., page numbers), and positional information (e.g., top and bottom lines) to identify headers and footers.

### **6.2. Removal of Identified Headers and Footers**
- **Rule:** 
  - Exclude detected headers and footers from chunk content to avoid redundancy and irrelevant information within chunks.
  - Keep meaningful variations or important instances when appropriate.

---

## **7. Table Splitting with Full Headers**

### **7.1. Handling Oversized Tables**
- **Rule:** 
  - If a table exceeds `hard_max_len`, split it into smaller tables.
  - Ensure that each split table includes the full header row to maintain context and readability.

### **7.2. Preserving Table Integrity**
- **Rule:** 
  - Maintain proper Markdown table syntax within each split to ensure tables render correctly.

---

## **8. Additional Enhancements**

### **8.1. Embedded Media Handling**
- **Rule:** 
  - Place large media embeds (e.g., videos, high-resolution images) in separate chunks to prevent inflating the size of other content.

### **8.2. Cross-Chunk References**
- **Rule:** 
  - Track and enhance links that point between chunks.
  - Maintain functional references between chunks (e.g., links pointing to sections in other chunks).
  - Include identifiers or anchors in links that correspond to target chunks.
  - Generate metadata about cross-references to facilitate navigation between related chunks.

### **8.3. Enhanced Metadata**
- **Rule:** 
  - Generate comprehensive metadata for each chunk, including:
    - Heading hierarchy and section structure
    - Chunk relationships (parent/child/sibling)
    - Cross-references to other chunks
    - Content types contained
    - Original document location
  - Include navigational aids to facilitate reconstruction of the document flow.

### **8.4. Accessibility Considerations**
- **Rule:** 
  - Preserve accessibility features such as alt text for images, proper heading hierarchies, and descriptive link texts within chunks.

### **8.5. Handling Custom Markdown Extensions**
- **Rule:** 
  - Detect and preserve syntax introduced by Markdown extensions or plugins (e.g., task lists, diagrams, LaTeX equations).
  - Ensure that extended syntax is not split across chunks to maintain functionality.

### **8.6. Consistent Line Endings and Whitespace**
- **Rule:** 
  - Normalize line endings and manage whitespace to ensure consistent formatting across chunks.
  - Remove excessive trailing spaces or blank lines that could disrupt Markdown structure.

### **8.7. Error Detection and Recovery**
- **Rule:** 
  - Implement syntax validation within each chunk to identify and rectify potential Markdown errors.
  - Provide fallback mechanisms to handle or skip malformed sections without halting the entire chunking process.

### **8.8. Parallel Processing for Performance**
- **Rule:** 
  - Utilize parallel processing (e.g., `ProcessPoolExecutor`) to handle multiple pages or large documents efficiently.
  - Implement chunking in a way that allows for concurrent processing of different document sections.
  - Ensure that the chunking process scales effectively with document size.
  - Include configurable parameters for controlling parallelization based on available system resources.

### **8.9. Testing and Validation**
- **Rule:** 
  - Develop comprehensive test cases covering various Markdown structures and edge cases.
  - Regularly validate that chunks render correctly across different Markdown parsers and platforms.

### **8.10. Customizable Chunking Rules**
- **Rule:** 
  - Allow users to define or adjust chunking behavior based on specific requirements or preferences.
  - Enable rule extensions to accommodate additional or customized chunking strategies.

### **8.11. Content Completeness**
- **Ensure** that no content is lost during the chunking process except for intentionally removed headers and footers.
- **Validate** that the total content of all chunks (excluding intentionally removed repeating headers/footers) equals the original document.
- **Perform** integrity checks before and after chunking to confirm all content is preserved.
- **Track** and report any content that might be inadvertently excluded during processing.

---

## **9. Summary of Comprehensive Rules**

### **9.1. Chunk Size Constraints**
- **Always** adhere to `hard_max_len`, never exceeding it under any circumstances.
- **Aim** to keep chunks between `min_chunk_len` and `soft_max_len`.
- **Merge** smaller chunks to meet `min_chunk_len`.
- **Split** oversized chunks at logical boundaries, ensuring no chunk exceeds `hard_max_len`.

### **9.2. Structural Integrity**
- **Use headings as primary chunking decision points**.
- **Keep headings with their content** whenever possible.
- **Preserve** all Markdown structural elements (headings, tables, lists, code blocks, etc.) within chunks.
- **Never split** critical elements unless absolutely necessary (as per `hard_max_len`).
- **Ensure** that any split tables include full headers for clarity.

### **9.3. Advanced Header and Footer Detection**
- **Identify** repeating headers and footers automatically using sophisticated pattern recognition.
- **Remove** detected headers and footers from chunk content to avoid redundancy.

### **9.4. Markdown Syntax Preservation**
- **Maintain** proper Markdown formatting within each chunk.
- **Avoid breaking** Markdown syntax across chunks to ensure correct rendering.

### **9.5. Enhanced Duplicate Content Management**
- **Detect and exclude** exact duplicates using hashing techniques.
- **Identify and manage** near-duplicate content using fuzzy matching algorithms.

### **9.6. Rich Metadata and References**
- **Generate detailed metadata** to aid in document reconstruction and navigation.
- **Track and enhance** cross-chunk references and links.
- **Maintain** functional relationships between chunks.

### **9.7. Accessibility and Usability**
- **Ensure** accessibility features are intact within chunks.
- **Preserve** logical heading hierarchies to support assistive technologies.

### **9.8. Performance Optimization**
- **Use parallel processing** for efficient handling of large documents.
- **Optimize chunking processes** for performance, especially for large documents.
- **Leverage** concurrency to enhance performance.

### **9.9. Customization and Flexibility**
- **Allow** users to customize chunking behavior based on specific needs.
- **Support** multiple Markdown flavors and custom extensions.

### **9.10. Robust Error Handling**
- **Implement** mechanisms to detect and recover from malformed Markdown.
- **Log** errors with sufficient context for troubleshooting.

### **9.11. Content Completeness**
- **Ensure** that no content is lost during the chunking process except for intentionally removed headers and footers.
- **Validate** that the total content of all chunks (excluding intentionally removed repeating headers/footers) equals the original document.
- **Perform** integrity checks before and after chunking to confirm all content is preserved.
- **Track** and report any content that might be inadvertently excluded during processing.

### **9.12. Embedded Chunk Metadata**
- **Enable** the option to include metadata directly within each chunk using YAML front matter.
- **Include** rich contextual information in the embedded metadata:
  - **Document Title**: The title of the original document
  - **Chunk ID**: The sequential number/identifier of the chunk
  - **Chunk Total**: Total number of chunks in the document
  - **Section Title**: The main heading of the current chunk
  - **Heading Hierarchy**: The full path of parent headings leading to the current chunk
  - **Previous/Next Chunks**: References to adjacent chunks for navigation
  - **Content Types**: List of Markdown element types contained in the chunk (tables, code blocks, etc.)
  - **Word Count and Character Count**: Size metrics for the chunk
  - **Position**: Approximate position in the original document (percentage)
  - **Parent Document**: Source document filename or identifier
- **Preserve** the original YAML front matter if present, merging it with the generated metadata.
- **Format** the metadata as standard YAML front matter at the beginning of each chunk for compatibility with existing Markdown processors.
- **Control** metadata inclusion via a configurable parameter to ensure backward compatibility.
- **Facilitate** document reconstruction by providing sufficient context within each chunk.

---

## **Implementation Considerations**

To effectively implement these comprehensive rules within the `MarkdownChunkingStrategy` class, consider the following strategies:

1. **Enhanced Pattern Recognition:**
   - Utilize advanced regular expressions and heuristics to automatically detect headers, footers, and other structural elements without relying on predefined templates.
   - Consider implementing machine learning approaches for pattern identification in very complex documents.

2. **Context-Aware Splitting:**
   - Develop logic that is aware of the current parsing context (e.g., inside a table, code block) to prevent inappropriate splits.
   - Prioritize heading-based chunking to maintain document section integrity.

3. **Dynamic Header Insertion:**
   - When splitting tables, dynamically insert header rows into each new table chunk to maintain clarity and structure.

4. **Parallel Processing Implementation:**
   - Implement a work-stealing algorithm for balanced distribution of chunking tasks.
   - Use thread pools or process pools based on the type of computation (I/O-bound vs. CPU-bound).

5. **Fuzzy Matching for Duplicates:**
   - Implement efficient algorithms for text similarity (e.g., MinHash, Levenshtein distance) to detect near-duplicates.
   - Balance accuracy with performance when determining similarity thresholds.

6. **Comprehensive Testing:**
   - Create extensive test suites that cover a wide range of Markdown features and edge cases to validate the robustness of the chunking strategy.
   - Include performance benchmarks for processing large documents.

7. **Configurability:**
   - Design the class to accept configurable parameters and extension points, allowing users to tailor the chunking behavior to their specific needs.
   - Provide sensible defaults for common use cases.

8. **Metadata Generation:**
   - Implement comprehensive metadata collection throughout the chunking process.
   - Design a metadata schema that supports document reconstruction and cross-chunk navigation.

9. **Logging and Reporting:**
   - Incorporate detailed logging to track the chunking process, identify issues, and provide insights for debugging and optimization.
   - Include performance metrics for monitoring and tuning.
