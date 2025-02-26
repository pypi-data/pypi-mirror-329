# commons-lib

This is a common library for dependencies that might be useful on Python Development.

It offers:
- A thread-safe Database Adapter + Data Migration executor powered by [SQLModel ORM (sqlalchemy)](https://sqlmodel.tiangolo.com/) and [Pydantic](https://pydantic.dev/);
- Local Cache database;
- Dynamic runtime import;
- Local/HTTP Remote Resource representation powered by [httpx](https://www.python-httpx.org/);
- Common Media Types;
- Currency support:
  - Currencies in ISO-4217 format powered by [pycountry](https://github.com/pycountry/pycountry/);
  - Currencies Quotation and Transfer Quotation from [Wise](https://wise.com/) and [Coinbase](https://coinbase.com/);
- [ ] Notification System (powered by [apprise](https://github.com/caronc/apprise)):
  - [x] SMTP tool for sending messages (to be replaced);
- [ ] Media Processors:
  - [ ] Document Processor;
  - [x] Image Processor;
  - [ ] Audio Processor;
  - [ ] Video Processor;
  - [ ] Subtitle Processor;

> ⚠️ This is under active development and might not be ready for production environments.
