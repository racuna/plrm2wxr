# plrm2wxr
Workouts from Progression posted to Pleroma reformated for WeightXReps
This Python script converts content posted on Pleroma (or other compatible services) into a format suitable for upload to the WeightXReps site. It processes workout data extracted from Pleroma and adjusts the format to follow WeightXReps conventions.

## Features

    Process Pleroma URL: Converts a Pleroma URL into an API call to retrieve the content of the post.
    Text formatting: Removes unnecessary characters, HTML tags (<br>), and adjusts the format for workout routines.
    Time replacement: Converts times from "min
    " format to seconds.
    Support for bodyweight exercises: Adds the BW (Bodyweight) prefix to calisthenics exercises.
    Remove # from line starts: Strips the # character if followed by a number at the beginning of a line.
    Save formatted content: Saves the formatted text into a .txt file, ready to be uploaded to WeightXReps.

## Requirements

To run this script, you need the following dependencies:

    Python 3.x
    requests: To make HTTP requests to the Pleroma API.
    beautifulsoup4: To process HTML content.
    textwrap: For handling text indentation.

You can install the dependencies using pip:

```
bash

pip install requests beautifulsoup4
```
## Usage
Running the script

    Clone this repository to your local machine.
    Run the script with the following command:

```
bash

python plrm2wxr.py <URL>
```

Where <URL> is the address of a Pleroma post containing your workout data.
Example

```
bash

python plrm2wxr.py https://pleroma.instance/notice/12345
```

The script will process the URL, extract and format the post content, and save the result in a file named plrm2wxr.txt in the same directory.
Workflow description

    Input URL: The script takes the Pleroma URL as an input argument.
    URL Transformation: Converts the viewable URL into a Pleroma API URL.
    Content Extraction: A request is made to the Pleroma API, and the post content is extracted in JSON format.
    Content Processing:
        Removes HTML tags (<br>) and replaces them with line breaks.
        Adjusts formatting by removing unwanted characters like #.
        Converts times in "min
        " format to seconds.
        Adds the BW prefix for calisthenics exercises.
    Output: The final content is saved to a text file called plrm2wxr.txt.

## Contributions

Contributions are welcome. If you would like to improve the script, please follow these steps:

    Fork the repository.
    Create a new branch (git checkout -b feature/new-feature).
    Make your changes and commit (git commit -m 'Add new feature').
    Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
