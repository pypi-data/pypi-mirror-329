# commons-lib

This is a common library for dependencies that might be useful on Python Development.

It offers:
- [x] A thread-safe Database Adapter + Data Migration executor
  - Implemented with [SQLModel ORM](https://sqlmodel.tiangolo.com/) (bonus: [Pydantic](https://pydantic.dev/));
- [x] Local Cache database;
- [x] Dynamic runtime import;
- [x] Local/HTTP Remote Resource representation (bonus: [httpx](https://www.python-httpx.org/));
- [x] Common Media Types;
- [ ] Notification System (powered by [apprise](https://github.com/caronc/apprise))
- [ ] Media Processors:
  - [ ] Document Processor;
  - [x] Image Processor;
  - [ ] Audio Processor;
  - [ ] Video Processor;
  - [ ] Subtitle Processor;

> ⚠️ This is under active development and might not be ready for production environments.