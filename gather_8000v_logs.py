---
 - name: Gather Logs for NEXUS switches
   hosts: nxos
   gather_facts: no

   tasks:

   - name: Log gathering command
     nxos_command:
       commands:
         #show the last 50 log entries
         - show logging last 50
         #show the hostname of the device
         #- show hostname
     register: config

   - name: Save output to logs.txt file
     copy:
       #content: "{{ config.stdout | replace('\\n', '\n')}}"
       #content: "{{ config.stdout }}"

       content: "{{ item }}"
       dest: "./logs/{{ inventory_hostname }}.log"
     with_items: "{{ config.stdout }}"
     #delegate_to: nxos


  
