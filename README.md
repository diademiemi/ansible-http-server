# ANSIBLE HTTP SERVER
I LOVE Ansible. A little too much? A little too much.
I wanted to see if I could serve HTTP requests with the new Event Driven Ansible.
Is this a good idea? Hell no. But I did it anyway.

## How to use
This definitely only works on Unix systems, not tested on Windows. Probably works in WSL. Why would you want to use this anyway? It's just a quirky experiment. Why are you seriously reading how to use this? You're never going to use this.

Since it serves files from the current working directory, you should clone this repo and run it from there.
It also needs an inventory, which I've provided in this repository, but you can bring your own, only needs to have a `localhost` host. (I've only tested it with localhost, and if you're running this against a production host, you're doing it wrong)

Install the Galaxy requirements
```bash
ansible-galaxy collection install .  # Or diademiemi.http_server if you're not in the repo
```

Install Ansible Rulebook
```bash
pip3 install ansible-rulebook

# OR
pip3 install -r requirements.txt
```

Run the Rulebook
```bash
ansible-rulebook -i inventories/local/hosts.yml -r diademiemi.http_server.http_server
```

You've now got a web server running on port 8080. Go to `http://localhost:8080` to see it in action! It serves the `index.html` file (or any requested file) in the `files` directory of your current working directory.

## How it works

This uses [Event Driven Ansible](https://www.ansible.com/blog/getting-started-with-event-driven-ansible/) to run a simple TCP socket server with a custom `event_source` plugin ([extensions/eda/plugins/event_source/tcp_server.py](extensions/eda/plugins/event_source/tcp_server.py)).This is called in the Rulebook ([extensions/eda/rulebooks/http_server.yml](extensions/eda/rulebooks/http_server.yml)). This plugin gets started through the Rulebook. When the Rulebook receives an event (A TCP connection from the plugin) it runs an Ansible Playbook.

The Ansible Playbook ([playbooks/response.yml](playbooks/response.yml)) receives the request and parses it, finds a file in the `files` directory, calls a Module ([plugins/modules/http_response.py](plugins/modules/http_response.py)) which receives a file descriptor over a Unix socket (`/tmp/ansible_http.sock`) (basically, gets the TCP socket to the client in place of the original process) and sends a response as defined in the Ansible Playbook.

Keep in mind, this barely works and is held together with hopes and prayers. It was a fun experiment though.

## Why this is funny
If you don't know Ansible, Ansible is a Configuration Management tool. You might think, that doesn't sound like a web server. You're right, it's not. But I made it one. Why? Because I can. And because I'm a little too obsessed with Ansible. Ansible is meant to configure remote hosts, and this new Event Driven Ansible framework is meant to react to outages and events in your infrastructure. But I made it serve HTTP requests. This is stupid.
Ansible has an extensive plugin system, and I wanted to see how far I could push it. This is the result. Using the new event framework I could make a TCP server, and with a little bit of duct tape and a lot of hope, I made it serve HTTP requests.