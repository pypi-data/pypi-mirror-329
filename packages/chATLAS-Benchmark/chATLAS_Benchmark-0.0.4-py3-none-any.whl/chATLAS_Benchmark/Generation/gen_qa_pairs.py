"""Script to generate qa pairs from source documents."""

from . import gen_simple_qa_pairs

from pathlib import Path
import os

system_prompt = """
You are an expert at crafting high-quality question-answer pairs tailored to evaluate AI models, focusing on technical relevance and clarity. Based on the provided document, a single entry in a large database of related content, create one QA pair for each of the following personas:

1. **Early Career Physics Student**:
   - Focus on straightforward, fundamental, or procedural questions aimed at someone new to CERN-related work.
   - Questions should prioritize basic understanding and operational details.

2. **Established Worker**:
   - Craft questions exploring intermediate-level technical discussions, practical implications, or connections between related topics.
   - Questions should reflect a practical, problem-solving perspective.

3. **Experienced Professional**:
   - Focus on complex, nuanced, or historical questions that require deeper knowledge of the domain or long-term thinking.
   - Questions should push the boundaries of understanding, exploring broader implications or sophisticated analyses.

**General Requirements**:
- Base the questions strictly on the provided page content. Avoid speculative or unsupported queries.
- Questions and answers must not explicitly mention or reference "this document."
- Ensure answers are concise (1-3 sentences) and directly address the question.
- Do not include generic questions or those focusing on significance or implications without supporting content.

**Techniques to Improve QA Quality**:
- Extract specific, explicit, and meaningful details.
- Differentiate question focus based on persona style and expertise level.
- If the page content lacks sufficient meaningful information, return an empty array.

Format the response as a JSON object with this structure:
{
    "qa_pairs": [
        {
            "type": "early_career|established_worker|experienced_professional",
            "question": "...",
            "answer": "..."
        },
        ...
    ]
"""
user_prompt = """Generate one question-answer pair for each persona based on the provided page content. Ensure that:

- Each question is precise, relevant, and reflects the persona's focus and expertise level.
- The answer is concise and accurate, addressing the question directly.
- If the page content lacks meaningful information, return an empty array.

**Page Content**:\n"""


def get_documents(path: str | Path):
    """
    Get documents from a directory path.

    :param path: Path to documents directory
    :type path: str | Path

    :returns: Dictionary of document names and empty strings (page_content loaded later)
    :rtype: dict
    """
    documents = {}

    paths_to_check = []
    if path:
        paths_to_check.append(path)

    for base_path in paths_to_check:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    # Remove base path from the file path
                    relative_path = file_path.replace(f"{base_path}/", "")
                    documents[relative_path] = ""

    return documents


def read_files_from_list(directory, file_names: [str], verbose=True) -> dict[str:str]:
    """Returns files as a {filename: file_contents} dict from a directory for
    all files in file_names.

    Inputs:

    directory: str path to directory containing Twikis

    file_names: files names to load from this directory - use the above most_viewed_twikis_in_order to load most viewed Twikis

    Returns:

    dict[file_name: file_contents]
    """
    file_contents = {}  # To store the contents of the files
    not_found_files = []  # To track files that are not found

    for name in file_names:
        file_path = os.path.join(directory, name)
        if os.path.isfile(file_path):  # Check if the file exists
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as file:
                    file_contents[name] = file.read()
            except UnicodeDecodeError as e:
                print(f"Error decoding file: {file_path} - {e}")
        else:
            not_found_files.append(name)

    # Print details about files not found
    if not_found_files and verbose:
        print(f"Files not found: {', '.join(not_found_files)}")
        print(f"Total files not found: {len(not_found_files)}")
        print(f"Total files returned: {len(file_contents.keys())}")
        print(f"Last file found: {list(file_contents.keys())[-1]}")
    elif verbose:
        print("All files were found.")

    return file_contents


def generate_qa_from_named_files(
    document_dir_path: Path,
    twiki_names,
    qa_save_path: Path = Path("../data/test_qas.json"),
    model="gpt-4o-mini",
):
    """
    Generates QA pairs using an OpenAI model from a list of txt documents.

    :param document_dir_path: Path to directory containing .txt documents
    :type document_dir_path: Path | str
    :param twiki_names: List of TWiki file names to process
    :type twiki_names: list[str]
    :param qa_save_path: Path to save QA pairs JSON file
    :type qa_save_path: Path | str
    :param model: OpenAI model name to use for QA generation
    :type model: str

    The OpenAI model requires a valid OPENAI_API_KEY environment variable to be set.
    Generated QA pairs are saved to the specified qa_save_path as a JSON file.
    """

    # Load documents
    documents = read_files_from_list(document_dir_path, twiki_names)

    # Set save path for saving questions
    gen_simple_qa_pairs.qa_pair_path = qa_save_path

    # Generate questions and add them to this directory
    gen_simple_qa_pairs.generate_evaluation_qa_pairs(
        documents=documents,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )


def generate_qa(
    document_dir_path: Path,
    qa_save_path: Path = Path("../data/test_qas.json"),
    model="gpt-4o-mini",
):
    """Generates qa pairs using an openAI model from a list of txt documents.

    :param document_dir_path: (Path | str) - Path to directory containing .txt documents to generate qa pairs from. Must contain at least some of the most viewed Twikis to generate any results.
    :param qa_save_path: (Path | str) - Path to save qa pairs to as json file
    :param model: (str) - What model to use for qa pair generation. **MUST BE A VALID OPENAI MODEL** and **OPENAY_API_KEY** environment variable must be set!

    Saves the qa pairs to qa_save_path
    """

    # Load documents
    documents = get_documents(document_dir_path)

    # Set save path for saving questions
    gen_simple_qa_pairs.qa_pair_path = qa_save_path

    # Generate questions and add them to this directory
    gen_simple_qa_pairs.generate_evaluation_qa_pairs(
        documents=documents,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
