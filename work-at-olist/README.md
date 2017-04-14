[![CircleCI](https://circleci.com/gh/ryukinix/work-at-olist-test.svg?style=svg)](https://circleci.com/gh/ryukinix/work-at-olist-test)
[![codecov](https://codecov.io/gh/ryukinix/work-at-olist-test/branch/master/graph/badge.svg?token=C6wyVSwO1b)](https://codecov.io/gh/ryukinix/work-at-olist-test)

# Description

Implementation of work-at-olist test about processing channels & categories for marketplaces. 

## Libs

* `Django` 1.11
* `Django Rest Framework` 3.6.2

## Environment

---
Computer: Notebook Dell D620
Operating System: Linux 4.7.10 @ Manjaro
Editors: Sublime Text, Emacs and Vim (in order of most used)
Python: 3.6.0
---

## CI

---
CI: CircleCI
Coverage: Codecov
---

# API REST Docs

Routes:

* GET `/api/channels/`
* GET `/api/channels/<channel_name>/`
* GET `/api/channels/<channel_name>/<category_name>/`

## Channel List
Retrieve a list of channels. Each entry have the fields `name` and `identifier`.

Example: GET `/api/channels/`
![channel-list](docs/channel-list.png)

## Channel Detail
Retrieve a list of all categories that belongs to a given channel. Return in nested mode
like a category tree ordered by parents and subcategories. Each entry has a `name`, `identifier` and may have a list of `subcategories` with this same properties described.

Example: GET `/api/channels/mercado-livre/`
![channel-detail](docs/channel-detail.png)


## Category Detail
Retrieve the parents and subcategories of given a category and its channel. A unique
entry with the `name`, and a list of `parents` and `subcategories` of the given category.

Example: GET `/api/channels/mercado-livre/computers/`
![category-detail](docs/category-detail.png)