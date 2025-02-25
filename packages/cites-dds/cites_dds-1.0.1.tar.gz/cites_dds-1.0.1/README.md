# CITES DDS Factory

Knihovna obsahuje factory pro přístup k datům CITES pomocí DDA 

Třída DdsFactory je typu singleton a používá se v rámci aplikace pro správu dokumentů 
Jsou implementovány všechny základní funkce čtení a zápisu dat. 

Knihovna neslouží ke stahování souborových příloh 

## Příklad použití

Instalace knihovny: 

    pip install cites-dds

Zařazení do kódu:

    from cites_dds.dds import DdsFactory

    CONFIG = {
      CONFIG_DDS_DOCUMENTS: {
        CONFIG_URL: 'https://abc.example.com',
        CONFIG_USERNAME: 'xxxxxxxxxxxxx',
        CONFIG_PASSWORD:  '*************',
        CONFIG_REPID:     'XXXXXXXXXXXXXXXA'
      },
      CONFIG_DDS_PERMITS: {
        CONFIG_URL: 'https://abc.example.com',
        CONFIG_USERNAME: 'xxxxxxxxxxxxx',
        CONFIG_PASSWORD:  '*************',
        CONFIG_REPID:     'XXXXXXXXXXXXXXXA'
      },
      CONFIG_DDS_STATEMENTS: {
        CONFIG_URL: 'https://abc.example.com',
        CONFIG_USERNAME: 'xxxxxxxxxxxxx',
        CONFIG_PASSWORD:  '*************',
        CONFIG_REPID:     'XXXXXXXXXXXXXXXA'
      },
      CONFIG_DDS_CERT_REG: {
        CONFIG_URL: 'https://abc.example.com',
        CONFIG_USERNAME: 'xxxxxxxxxxxxx',
        CONFIG_PASSWORD:  '*************',
        CONFIG_REPID:     'XXXXXXXXXXXXXXXA'
      }
    }

    DDS_FACTORY = DdsFactory(config=CONFIG)
