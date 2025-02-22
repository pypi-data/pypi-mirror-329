
# Net Command

Net Command 是一个类似 Ansible 的批量 SSH 操作工具，使用 `netmiko` 作为核心库。它支持通过 YAML 配置文件管理设备清单和批量配置文件，并支持多进程执行任务。

## 安装

使用 `poetry` 安装依赖：

```bash
poetry install
```

## 使用方法

### 查看设备清单

使用 `--list` 参数查看设备清单的字典输出：

```bash
netcmd -i inventory.yaml --list
```

### 执行 Playbook

指定设备清单和 Playbook 文件来执行任务：

```bash
netcmd -i inventory.yaml playbook.yaml
```

## 配置文件格式

### 设备清单 (`inventory.yaml`)

设备清单文件使用 YAML 格式，示例如下：

```yaml
all:
  vars:
    port: 22
    user: 'admin'
    password: 'password@123456'
    vendor: 'hp_comware'

box_as:
  hosts:
    192.168.56.2:
    192.168.56.3:
    192.168.56.4:
```

### Playbook (`playbook.yaml`)

Playbook 文件使用 YAML 格式，示例如下：

```yaml
- name: H3C NTP Configuration
  hosts: box_as
  num_processes: 2
  vars:
    host: "{{ host }}"
    port: "{{ port }}"
    username: "{{ user }}"
    password: "{{ password }}"
  tasks:
    - name: Check NTP status on H3C devices
      when: vendor == 'hp_comware'
      commands: 
        - display ntp status
```

## 测试

使用 `pytest` 运行测试：

```bash
pytest
```

## 贡献

欢迎提交问题和贡献代码！

## 许可证

本项目使用 MIT 许可证。
