# Change Log

<!-- GENERATOR_PLACEHOLDER -->

## 0.0.8

### Fixed
  - Fix a javascript error in toolbar.js where trying to get the toolbar 
    buttons caused an error when no user is logged in since then no buttons
    are rendered. So the button variables where null.

## 0.0.7

### Changed
  - Remove jQuery dependency: Change toolbar.js from jquery to plain javascript

## 0.0.6

### Fixed 
  - Add missing translation *.mo files

### Fixed
  - Fix search-form extended search button icon

## 0.0.5

### Fixed
  - Fix search-form extended search button icon

## 0.0.4

### Fixed
  - Remove local logout view and use from django.contrib.auth directly

## 0.0.3

### Fixed 
- Fix more left-overs from local code #1
  - Changed form url from "core:search" to "lite_cms_core:search"
  - Fix logout url by providing logout view 
  - Remove icon dependency and copy used icons to project

## 0.0.2

### Fixed
- Rename forgotten "core" static directory to "lite_cms_core"

## 0.0.1

### Initial
- Initial version