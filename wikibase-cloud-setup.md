# Setting Up a Wikibase Instance on Wikibase.cloud

This guide walks you through creating your own Wikibase instance using [Wikibase.cloud](https://www.wikibase.cloud), the hosted platform by Wikimedia Deutschland. No installation or technical setup is required — everything runs in your browser.

---

## What is Wikibase.cloud?

Wikibase.cloud is a free hosted service that lets you create your own collaborative knowledge base using the same open-source software that powers Wikidata. Each instance comes with:

- A full **Wikibase** wiki for creating items and properties
- A **SPARQL Query Service** for querying your data
- **QuickStatements** for batch importing data
- A **REST API** for programmatic access
- Support for images from **Wikimedia Commons**
- The ability to import entities from **Wikidata**

> The service is currently in **Open Beta** and is free to use.

---

## Step 1 — Create an account

1. Go to [https://www.wikibase.cloud](https://www.wikibase.cloud)
2. Click **Sign up**
3. Enter your email address and choose a password
4. Verify your email address via the confirmation link sent to your inbox

---

## Step 2 — Create a Wikibase instance

Once logged in:

1. Click **Create a Wikibase**
2. Fill in the form:
   - **Wikibase name** — this becomes part of your URL (e.g. `my-research.wikibase.cloud`)
   - **Username** — the admin username for your wiki (separate from your wikibase.cloud login)
   - **Purpose** — briefly describe what you intend to use it for (e.g. "workshop practice instance for mixed-methods research")
   - **Expected lifespan** — how long you plan to use it
   - **Target audience** — e.g. researchers, students
3. Click **Create** and wait a minute or two for provisioning to complete
4. A few seconds after creation you will receive an email with a **temporary password** and a link to reset it — check your inbox and set a permanent password before logging in to your wiki

> Choose your Wikibase name carefully — it cannot be changed after creation.

---

## Step 3 — Access your instance

Once created, your instance is available at:

| Service | URL pattern |
|---|---|
| Wikibase wiki | `https://<your-name>.wikibase.cloud` |
| SPARQL Query Service | `https://<your-name>.wikibase.cloud/query` |
| QuickStatements | `https://<your-name>.wikibase.cloud/tools/quickstatements` |

Log in to your wiki using the same credentials you used to sign up on Wikibase.cloud.

---

## Step 4 — Explore your instance

Once logged in to your wiki, you can:

- **Create items** — go to **Special:NewItem** to add your first entity
- **Create properties** — go to **Special:NewProperty** to define relationships
- **Run SPARQL queries** — open the Query Service at `/query` and write queries against your data
- **Import from Wikidata** — use the built-in import tool to pull existing entities

---

## Key things to know

- Wikibase.cloud instances are **publicly visible** by default — do not store sensitive or private data
- The service is operated by **Wikimedia Deutschland** and governed by their [Terms of Use](https://www.wikibase.cloud/help/wikibase-cloud/terms-of-use) and [Hosting Policy](https://www.wikibase.cloud/help/wikibase-cloud/hosting-policy)
- Instances that violate the hosting policy (e.g. spam, private data, inactivity) may be suspended
- This is a **beta service** — do not rely on it for production or archival purposes without a backup strategy

---

## Further reading

- [Wikibase.cloud help centre](https://www.wikibase.cloud/help)
- [Wikibase on MediaWiki.org](https://www.mediawiki.org/wiki/Wikibase)
- [Wikibase ecosystem directory — wikibase.world](https://wikibase.world)
- [Community Telegram group](https://t.me/joinchat/HGjGexZ9NE7BwpXzMsoDLA)
