# HOWTO

How can I install Python in an isolated directory—for example, /data/python/—without affecting the existing environment?

To install Python in a specific, isolated directory (like `/data/python/`) without touching the system's `/usr/bin` or `/usr/lib` directories, you cannot use `dnf`. 
Package managers are designed to install software into standard system paths.

The only way to achieve a truly isolated installation in a custom directory is to **compile Python from source**.

### The Ansible Playbook: Source Installation

This playbook will download the Python source code, configure it to install into your custom directory, and compile it.

```yaml
---
- name: Install Isolated Python on RHEL 9
  hosts: all
  become: yes
  vars:
    # These can be overridden via -e
    python_version: "3.12.2" 
    install_dir: "/data/python"

  tasks:
    - name: Install build dependencies
      dnf:
        name:
          - gcc
          - make
          - openssl-devel
          - bzip2-devel
          - libffi-devel
          - zlib-devel
          - readline-devel
          - sqlite-devel
          - tk-devel
          - gdbm-devel
          - xz-devel
        state: present

    - name: Create installation directory
      file:
        path: "{{ install_dir }}"
        state: directory
        mode: '0755'

    - name: Download Python source code
      get_url:
        url: "https://www.python.org/ftp/python/{{ python_version }}/Python-{{ python_version }}.tgz"
        dest: "/tmp/Python-{{ python_version }}.tgz"

    - name: Extract Python source
      unarchive:
        src: "/tmp/Python-{{ python_version }}.tgz"
        dest: "/tmp/"
        remote_src: yes

    - name: Configure, Build and Install Python
      shell: |
        cd /tmp/Python-{{ python_version }}
        ./configure --prefix={{ install_dir }} --enable-optimizations
        make -j $(nproc)
        make altinstall
      args:
        creates: "{{ install_dir }}/bin/python{{ python_version }}"

    - name: Verify isolated installation
      command: "{{ install_dir }}/bin/python{{ python_version }} --version"
      register: isolated_python_check
      changed_when: false

    - name: Print Python version
      debug:
        msg: "Isolated Python installed at {{ install_dir }}. Version: {{ isolated_python_check.stdout }}"

    - name: Cleanup source files
      file:
        path: "{{ item }}"
        state: absent
      with_items:
        - "/tmp/Python-{{ python_version }}.tgz"
        - "/tmp/Python-{{ python_version }}"
```

### How to run it

Since we are compiling from source, you must provide the **full version number** (e.g., `3.12.2` instead of just `3.12`).

```bash
ansible-playbook -i hosts.ini install_isolated_python.yml -e "python_version=3.12.2 install_dir=/data/python"
```

### Technical Explanations:

1.  **`--prefix={{ install_dir }}`**: This is the magic flag. It tells the Python installer: "Do not put files in `/usr/local/bin`, put everything (binaries, libraries, 
include files) inside `/data/python`."
2.  **`--enable-optimizations`**: This makes Python run about 10-20% faster by running profile-guided optimizations (PGO). *Note: This makes the compilation process take 
longer.*
3.  **`make altinstall`**: We use `altinstall` instead of `install` to prevent the build process from accidentally creating symlinks that could overwrite the system's 
default `python` binary.
4.  **`make -j $(nproc)`**: This tells the compiler to use all available CPU cores on the VM to speed up the build process.
5.  **Build Dependencies**: Compiling Python requires several C libraries (like `openssl-devel` for the `ssl` module and `libffi-devel` for `ctypes`). Without these, 
your isolated Python will be missing critical features.

### How to use this isolated Python

Because this Python is not in the system's global `PATH`, the command `python` or `python3` will still point to the RHEL system version. To use your isolated version, 
you have three choices:

**1. Call it by the full path (Safest):**
```bash
/data/python/bin/python3.12 -m pip install requests
/data/python/bin/python3.12 my_script.py
```

**2. Create a Virtual Environment from the isolated version:**
This is the industry best practice.
```bash
/data/python/bin/python3.12 -m venv /data/my_project_env
source /data/my_project_env/bin/activate
# Now 'python' is your isolated 3.12 version
```

**3. Update the User PATH (Permanent for one user):**
Add this to the user's `~/.bashrc`:
```bash
export PATH="/data/python/bin:$PATH"
```

---

