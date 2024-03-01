## Task 2: Identifying and explaining difficult concepts

The goal of this task is to decide which concepts in scientific abstracts require explanation and contextualization in order to help a reader understand the scientific text.

The task has two steps:
i) to retrieve up to 5 difficult terms in a given passage from a scientific abstract
ii) to provide a definition or an explanation or both of these difficult terms.

The corpus of Task 2 is based on the sentences in high-ranked abstracts to the requests of Task 1.

### Evaluation:

We will evaluate complex concept spotting in terms of their complexity and the detected concept spans.

We will automatically evaluate provided explanations by comparing them to references (e.g. ROUGE, cosine similarity, etc.).

In addition, we will manually evaluate the provided explanations in terms of their usefulness with regard to a query as well as their complexity for a general audience.

Note that the provided explanations can have different forms, e.g. abbreviation deciphering, examples, use cases, etc.

### Simplified explanation of the vectorization process in the context of transformer-based models like GPT-4:

**Tokenization:**

- The first step in processing text is tokenization, where the input text is split into manageable pieces, such as words, subwords, or characters.

- These tokens are then mapped to unique integers based on a predefined vocabulary.

- This process allows the model to handle a wide range of vocabulary, including rare words, by breaking them down into smaller, more common subwords or characters.

**Embedding Layer:**

- After tokenization, each integer token is passed through an embedding layer, which converts these integers into fixed-size vectors.

- These embedding's are learned during the model's training process and are designed to capture semantic information about the words or subwords they represent.

- This means that similar words should have similar vectors, encoding aspects of their meaning.

**Positional Encoding:**

- Since transformer models do not inherently process sequential data in order, positional encoding's are added to the embedding's to

- give the model information about the order of tokens. These encoding's are usually vectors that are added or concatenated to the embedding vectors,

- ensuring that the model can consider the sequence of words in understanding and generating text.

**Contextualized Embedding's:**

- Through the multiple layers of the transformer, including attention mechanisms, the initial embedding's are processed and updated.

- This processing allows the model to create contextualized embedding's, where the representation of each word or token reflects not just its inherent meaning but also the meaning it has in the specific context of the input text. This is a key feature that enables models like GPT-4 to understand nuanced language, ambiguity, and complex relationships between words.
