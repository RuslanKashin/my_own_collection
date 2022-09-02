#!/usr/bin/python

# Copyright: (c) 2022, Ruslan Kashin <ruslan.kashin@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: create_file

short_description: This is homework for Netology.

version_added: "1.0.0"

description: This is 8.4 homework for Netology, DVPSPDC-3.

options:
    path:
        description: Path to new file.
        required: true
        type: str
    content:
        description: New file content.
        required: true
        type: str

author:
    - Ruslan Kashin (@RuslanKashin)
'''

EXAMPLES = r'''
# Create file
- name: Create file with content
  create_file:
    path: "/tmp/my_file_name.txt"
    content: "My file content"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
message:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'File /tmp/my_file_name.txt was created successfully!'
'''

from ansible.module_utils.basic import AnsibleModule

import os
import os.path

def main():

    module_args = {
        "path": {"type": "str", "required": True},
        "content": {"type": "str", "required": True},
    }

    result = {
        "message": "Wrong path. File not accessible."
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )    
    
    if module.check_mode:
        module.exit_json(**result)

    # file handling
    #---------------------------------------------------
    my_path = module.params["path"]
    my_content = module.params["content"]
    
    if os.path.isfile(my_path):
       read_file = open(my_path,"r")
       if my_content == read_file.read():
          result["message"] = "A file with this content already exists. Creation is not required."
          read_file.close()
       else:
          read_file.close()
          write_file = open(my_path, "w+")
          write_file.write(my_content)
          write_file.close()
          result["message"] = "File content updated."
    else:
       try:
          new_file = open(my_path, "w+")
       except IOError:
          result["message"] = "Wrong path. File not accessible."
       else:
          new_file.write(my_content)
          result["message"] = "Created a new file with the given content."
          new_file.close()
    #----------------------------------------------------     

    module.exit_json(**result)    

if __name__ == '__main__':
    main()

