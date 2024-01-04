# Prometheus IP Discovery

Simple frankenstein Python script that scans network subnet using `nmap` for currently live hosts
and then generate Prometheus target files that can be read using Prometheus `file_sd_configs`.

## Preresquites

- Python (3.x)
- nmap

## Usage

1. Clone the repository
``` bash
git clone https://github.com/ndkprd/prometheus-ip-discovery.git
```

2. Navigate to the project directory
``` bash
cd prometheus-ip-discovery
```

3. Run the script
```
python prom-ip-discovery.py --subnet <your_subnet> --label <label_name1=label_value1> <label_name2=label_value2> ...
```

Replace `<your_subnet>` with target subnets (e.g., *10.10.10.0/24*) and then add labels as you like.

4. You can check the generated target file in `output/discovered_targets.yml'.

## Example

``` bash
python prom-ip-discovery.py --subnet 10.10.10.0/24 --label env=prod app=myapp

```

## License

This project is licensed under [MIT license](https://mit-license.org/).
