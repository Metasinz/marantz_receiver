"""
Commands and operators used by Marantz.

CMDS[domain][function]

Majority of Marantz commands use ':' as operator although there are also some
multi-zone commands that use '='

"""

CMDS = {
    'main':
        {
            'mute':
                {'cmd': 'AMT',
                 'supported_operators': [':']
                 },
            'power':
                {'cmd': 'PWR',
                 'supported_operators': [':']
                 },
            'volume':
                {'cmd': 'VOL',
                 'supported_operators': [':']
                 },
            'source':
                {'cmd': 'SRC',
                 'supported_operators': [':']
                 },
            'autostatus':
                {'cmd': 'AST',
                 'supported_operators': [':']
                 }
        }
}