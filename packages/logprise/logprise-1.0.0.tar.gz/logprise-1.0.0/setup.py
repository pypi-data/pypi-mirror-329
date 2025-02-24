# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logprise']

package_data = \
{'': ['*']}

install_requires = \
['apprise', 'loguru']

setup_kwargs = {
    'name': 'logprise',
    'version': '1.0.0',
    'description': 'A package integrating loguru and apprise for logging and notifications',
    'long_description': '# Logprise\n\nLogprise is a Python package that seamlessly integrates [loguru](https://github.com/Delgan/loguru/) and [apprise](https://github.com/caronc/apprise) to provide unified logging and notification capabilities. It allows you to automatically send notifications when specific log levels are triggered, making it perfect for monitoring applications and getting alerts when important events occur.\n\n## Features\n\n- Unified logging interface that captures both standard logging and loguru logs\n- Automatic notification delivery based on configurable log levels\n- Batched notifications to prevent notification spam\n- Flexible configuration through apprise\'s extensive notification service support\n- Easy integration with existing Python applications\n\n## Installation\n\n```bash\npip install logprise\n```\n\nOr if you\'re using Poetry:\n\n```bash\npoetry add logprise\n```\n\n## Quick Start\n\nHere\'s a simple example of how to use Logprise:\n\n```python\nfrom logprise import logger\n\n# Your logs will automatically trigger notifications\nlogger.info("This won\'t trigger a notification")\nlogger.warning("This won\'t trigger a notification")\nlogger.error("This will trigger a notification")  # Default is ERROR level\n\n# Notifications are automatically sent when your program exits\n```\n\n## Configuration\n\n### Notification Services\n\nLogprise uses Apprise for notifications, which supports a wide range of notification services. Create an `apprise.txt` file in one of the default configuration paths:\n\n- `~/.apprise`\n- `~/.config/apprise`\n\nExample configuration:\n\n```text\nmailto://user:pass@gmail.com\ntgram://bot_token/chat_id\nslack://tokenA/tokenB/tokenC/#channel\n```\n\nSee [Apprise\'s configuration guide](https://github.com/caronc/apprise/wiki/config#cli) for the full list of supported services and their configuration.\n\n### Notification Levels\n\nYou can set the minimum log level that triggers notifications:\n\n```python\nfrom logprise import appriser, logger\n\n# Using string level names\nappriser.notification_level = "WARNING"  # or "DEBUG", "INFO", "ERROR", "CRITICAL"\n\n# Using integer level numbers\nappriser.notification_level = 30  # WARNING level\n\n# Using loguru Level objects\nappriser.notification_level = logger.level("ERROR")\n```\n\n### Manual Notification Control\n\nWhile notifications are sent automatically when your program exits, you can control them manually:\n\n```python\nfrom logprise import appriser\n\n# Clear the notification buffer\nappriser.buffer.clear()\n\n# Send notifications immediately\nappriser.send_notification()\n```\n\n## Contributing\n\nTo contribute to the project:\n\n```bash\n# Clone the repository\ngit clone https://github.com/yourusername/logprise.git\ncd logprise\n\n# Install dependencies\npoetry install\n\n# Run tests\npoetry run pytest\n```\n\nContributions are welcome! Please feel free to submit a Pull Request.\n\n## License\n\nThis project is licensed under the MIT License - see the LICENSE file for details.',
    'author': 'Steven Van Ingelgem',
    'author_email': 'steven@vaningelgem.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/svaningelgem/logprise',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
