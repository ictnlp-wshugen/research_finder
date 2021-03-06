A command-line based paper search engine

#### Features
- Support multiple keyword arguments
- Support multiple exclusive keyword arguments
- Support cached query result
- Support Offline data search
- NLP relevant data (The most recent Conferences on NLP like ACL/COLING/EMNLP etc.) included
- Support add new data
- Support for Preceding/Journal/Transaction papers
- Only allowed for non-commercial use

#### Definition
- Data: An url that corresponding to a DBLP url contains paper list like 'https://dblp.uni-trier.de/db/conf/acl/acl2018-1.html'
- Subkey: a partial data like 'ACL'

#### Usage
- Add new data using dblp.py
- Show data list using ***papers.py -l*** (The first time to run would be slower for building a cache)
- Search paper titles using ***papers.py -q -s "keyword1" ["keyword2"] -es "exclude keyword1" ["exclude keyword2"] -sk "subkey of data"***

#### Example, filter 'Neural Machine Translation' from ICLR Proceedings
```bash
./papers.py -q -s "Neural Machine Translation" -sk iclr
```
