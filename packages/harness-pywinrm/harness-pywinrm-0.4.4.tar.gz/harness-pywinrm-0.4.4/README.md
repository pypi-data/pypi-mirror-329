# harness-pywinrm

CLI library for interacting with Windows machines via the Windows Remote Management (WinRM) service, using Kerberos authentication.

## Installation

To install the library, run:

```python
pip install harness-pywinrm
```

## Usage

Here’s an example of how to use it:

```python

# Create file_with_command file with command to be executed on remote machine

# HTTPS - 5986
harness-pywinrm -e https://hostname.domain.com:5986/wsman -u Principal@Realm -s false -env {KEY1=VALUE1,KEY2=VALUE2} -w %USERPROFILE% -t 1800000 -cfile file_with_command

# HTTP - 5985
harness-pywinrm -e http://hostname.domain.com:5985/wsman -u Principal@Realm -s false -env {KEY1=VALUE1,KEY2=VALUE2} -w %USERPROFILE% -t 1800000 -cfile file_with_command
```