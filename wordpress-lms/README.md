# Adoption Curriculum — WordPress + Tutor LMS (local)

A one-command local setup that spins up a WordPress site with **Tutor LMS**
installed and a starter adoption curriculum seeded in. Use it to build and
preview your courses before paying for hosting.

## What you need first

**Docker Desktop** installed and running.
- Mac: https://www.docker.com/products/docker-desktop/  → install → open it (whale icon in the menu bar)
- Windows: same link → install → open Docker Desktop

That's the only prerequisite. You don't need to install PHP, MySQL, or WordPress
yourself — Docker handles all of it.

## Start it

Open a terminal, `cd` into this folder, and run:

```bash
./setup.sh
```

The first run downloads WordPress and takes a couple of minutes. When it
finishes it prints your site address and admin login. By default:

- **Site:** http://localhost:8080
- **Admin:** http://localhost:8080/wp-admin
  - user: `admin`
  - password: `changeme-admin-pass`

Then log in, open **Tutor LMS** in the left menu, and you'll see the seeded
course ready to edit.

> Change the admin password (and the DB passwords) by copying `.env.example`
> to `.env` and editing it **before** your first run. `.env` is gitignored so
> your real passwords never get committed.

## Everyday commands

| Command | What it does |
|---|---|
| `./setup.sh` | Start the site (and install it on first run) |
| `./setup.sh stop` | Stop the site — **keeps** all your courses and data |
| `./setup.sh seed` | Re-run curriculum seeding (after editing `seed-curriculum.php`) |
| `./setup.sh reset` | **Delete everything** and start clean (asks for confirmation) |

Your data lives in Docker volumes, so `stop` then `./setup.sh` again brings
back exactly what you had.

## Editing the curriculum

Two ways, use whichever you prefer:

1. **In the browser (easiest):** log in → Tutor LMS → Courses → edit. Add
   topics, lessons, quizzes, videos, etc. This is where the real authoring
   happens.
2. **In code (for bulk structure):** edit `seed-curriculum.php` — it's a plain
   list of courses → topics → lessons. Then run `./setup.sh seed`. Re-running
   is safe: anything already there (matched by title) is skipped, not
   duplicated.

The seeded course is just a skeleton placeholder — replace its modules and
lessons with your own material.

## Files in this folder

| File | Purpose |
|---|---|
| `docker-compose.yml` | Defines the WordPress + database containers |
| `setup.sh` | Installs WordPress + Tutor LMS and seeds courses |
| `seed-curriculum.php` | The curriculum structure (edit this) |
| `.env.example` | Template for site title, admin login, ports, DB passwords |

## When you're ready to go live

This local setup is for building and previewing. To put the course online for
real students you'll move to a WordPress host. The short version:

1. Sign up for a WordPress host (most have a one-click WordPress install).
2. Install the **Tutor LMS** plugin from the WordPress plugin directory.
3. Recreate your courses there, or export/import using a migration plugin
   (e.g. All-in-One WP Migration) to copy this local site up to the host.

Ask and I'll write you a step-by-step going-live guide for whichever host you
choose.
