# External Applications

The External Applications app is a contrib module for GeoNode.
The app is compatible with GeoNode `v5.0.x`.

The app adds a model `ExternalApplication` which extends from `GeoApp`.
It integrates as a regular GeoNode resource type, so it is indexed, permission-checked, and filterable via the GeoNode REST API (`/api/v2/resources/?filter{resource_type.in}=externalapplication`) just like Datasets, Maps, or Dashboards.

Browsing and creating external applications happens on a dedicated page (`/externalapplications`) provided by this app, rather than through GeoNode's built-in MapStore catalogue/search UI. See [Known limitations](#known-limitations) below for why.

## Installation and Configuration

To activate the external application app, add the following to the `settings.py`:

```py
INSTALLED_APPS += ( 'externalapplications', )
EXTERNAL_APPLICATION_MENU_FILTER_AUTOCREATE = os.getenv('EXTERNAL_APPLICATION_MENU_FILTER_AUTOCREATE ', False)
```

Create database migrations and apply them via:

```sh
python manage.py makemigrations
python manage.py migrate
```

### Add a Navbar Menu Entry

If you want the app to create a navbar menu entry linking to `/externalapplications` automatically, set `EXTERNAL_APPLICATION_MENU_FILTER_AUTOCREATE=True`.

In case you want to manually add such an entry, use the GeoNode admin.
First create a `Menu` _External Application_ which you put under placeholder `TOPBAR_MENU_LEFT`.
After that, create a `MenuItem` under that `Menu` pointing at the URL `/externalapplications`.

## Working with External Applications

`/externalapplications` lists all external applications the current user is allowed to view, with pagination, fetched directly from the GeoNode REST API. Authenticated users see a "Register External Application" button there, which leads to `/externalapplications/create` — a simple form to set title, abstract, target URL, and an optional thumbnail.

Each entry links out via an "Open external application" button, which opens the registered `url` directly (in a new tab).

Editing an external application can be done only via the admin interface where all attributes can be changed.
To update the thumbnail you have to upload the new thumbnail by hand and change the thumbnail URL.

### Frontend implementation

The `/externalapplications` page is a plain Django template (no MapStore/React dependency from GeoNode core). Its resource grid is implemented with React 18 and Chakra UI v3, loaded directly as ES modules from `esm.sh` via an `importmap` — no JS build step (webpack/vite/npm) is required by this app or the surrounding GeoNode project. This does mean the page requires the browser to reach `esm.sh` at runtime; for air-gapped/intranet-only deployments, these CDN URLs would need to be swapped for self-hosted, pre-built assets.

## Known limitations

GeoNode 5.0.x's MapStore-based catalogue UI (`ResourcesGrid`, used on `/catalogue/#/`, `/datasets`, `/documents`, etc.) keeps a hardcoded, closed registry of renderable resource types (`ResourceUtils.js`'s `getResourceTypesInfo()`), and there is currently no supported extension point for third-party resource types to register into it. A resource whose `resource_type` isn't in that registry crashes the card-rendering step (`parseCatalogResource`) with an unhandled `TypeError`, which the UI silently turns into an "unavailable" empty state.

As a result, `externalapplication` resources:
- do **not** render inside GeoNode's shared catalogue pages or search UI, even though they are fully queryable via the REST API;
- are **not** linked to via `/catalogue/#/<type>/<pk>`-style detail URLs (GeoNode's standard resource detail links), since those hit the same crash.

This is why this app ships its own dedicated `/externalapplications` list/create pages instead of integrating into the shared MapStore catalogue, and why `ExternalApplication.get_absolute_url()` points straight at the external `url` rather than at a GeoNode detail page. If GeoNode/`geonode-mapstore-client` adds a registration hook for custom resource types in a future release, the catalogue integration removed during the 5.0.x migration (see git history) could be reinstated.

## Removing External Application App

Before removing the external application app, you have to delete all external applications from the database.
Open the Django shell and execute the following python tasks:

```py
python manage.py shell
from externalapplications.models import ExternalApplication

# Delete all instances from the geonode database
for d in ExternalApplication.objects.all(): d.delete()
```

After removing all instances, you can revert the migrations via the management command:

```sh
python manage.py migrate externalapplications zero
```

Once, all external applications have been deleted the app can be removed by deleting it from the `INSTALLED_APPS` in the `settings.py`.

## Funding

This contrib app was funded by

| Logo | Funding Organization |
|------|----------------------|
| <img alt="Thünen Logo" align="middle" height="50" src="https://www.thuenen.de/_assets/9c8c8373163efb014a59249bdf796e91/Graphics/SVG-Logo.svg"/> | [Thünen-Institute](https://www.thuenen.de) |
| <img alt="ZALF Logo" align="middle" height="50" src="https://www.zalf.de/_layouts/15/images/zalfweb/logo_zalf.png"/> | [Leibniz Centre for Agricultural Landscape Research](https://www.zalf.de/) |
