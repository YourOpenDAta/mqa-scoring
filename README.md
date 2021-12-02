# mqa-scoring

The Metadata Quality Assurance (MQA) methodology is defined by the data.europa.eu consortium with the aim of improving the accessibility of datasets published on EU open data portals. It specifies several indicators that help to improve the quality of the metadata harvested by the data.europa.eu portal.

Mqa-scoring is a tool that calculates the score a metadata obtains according to the MQA indicators. The tool also verifies that the requirements specified by the MQA for each indicator are met.

## Installation

`pip install -r requirements.txt`

## Usage

`python mqa-scoring.py -h`


usage: mqa-scoring.py [-h] -f FILE

Calculates the score obtained by a metadata according to the MQA methodology specified by data.europa.eu

optional arguments:

  -h, --help            show this help message and exit
  
  -f FILE, --file FILE  RDF file to be validated

## Requirements

- RDF file to be validated is mandatory. Up to now only support rdf+xml format.
- Install the rdflib library beforehand. In windows environments it is suggested to use version 5.x because version 6.x has some problems with directory path specification.
- The edp-vocabularies directory is a clone of the data.europa.eu GitLab repository vocabulary. It should be updated in case there are changes in the vocabularies.

## Example

```
python mqa-scoring.py -f ./rdf-examples/example-UPM-1.rdf
```
