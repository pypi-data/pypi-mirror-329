# bird-ospf-map

OSPF connection parser and maybe later even map generator


## Usage

```bash
poetry env activate
poetry install
ssh router sudo birdc show ospf state all ngn | poetry run bird_ospf_map -c ~/.bird-ospf-map.yaml
```


## Prerequisities
 * Bird2 with OSPF running


## Resources
 * We generate the graph using [the `Mermaid` library](https://mermaid.js.org/syntax/flowchart.html).

