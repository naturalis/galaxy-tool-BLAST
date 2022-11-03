# galaxy-tool-BLAST
Wrapper for BLASTn; perform Blast searches and find the associated taxonomy.  

## Installation  
### Manual  
Clone this repo in your Galaxy ***Tools*** directory:  
`git clone https://github.com/naturalis/galaxy-tool-BLAST`  

Make the scripts executable:  
`chmod 755 galaxy-tool-BLAST/blastn.sh`  
`chmod 755 galaxy-tool-BLAST/blastn_wrapper.py`  

Append the file ***tool_conf.xml***:    
`<tool file="/path/to/Tools/galaxy-tool-BLAST/blastn.xml" />`  

### Ansible
Depending on your setup the [ansible.builtin.git](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html) module could be used.  
[Install the tool](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html#examples) by including the following in your dedicated ***.yml** file:  

`  - repo: https://github.com/naturalis/galaxy-tool-BLAST`  
&ensp;&ensp;`file: blastn.xml`  
&ensp;&ensp;`version: master`  

## Create Blast databases  
See the [wiki](https://github.com/naturalis/galaxy-tool-BLAST/wiki) for creation of reference databases.  
