#!/usr/bin/env bash
#
# One-command setup for a local WordPress + Tutor LMS site for the adoption curriculum.
#
#   ./setup.sh            # start everything and install WordPress + Tutor LMS + seed courses
#   ./setup.sh reset      # DESTROY the site (database + files) and start fresh
#   ./setup.sh stop       # stop the containers (keeps your data)
#   ./setup.sh seed       # re-run only the curriculum seeding step
#
set -euo pipefail
cd "$(dirname "$0")"

# Load .env (create it from the example on first run).
if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example (using local-safe defaults)."
fi
set -a; source .env; set +a

WP_PORT="${WP_PORT:-8080}"
SITE_URL="${SITE_URL:-http://localhost:${WP_PORT}}"
SITE_TITLE="${SITE_TITLE:-Adoption Curriculum}"
ADMIN_USER="${ADMIN_USER:-admin}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-changeme-admin-pass}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@example.com}"

# Pick "docker compose" (v2) or "docker-compose" (v1).
if docker compose version >/dev/null 2>&1; then DC="docker compose"; else DC="docker-compose"; fi

# Run a wp-cli command inside the tools container. Naming the service explicitly
# starts it even though it's behind the "tools" profile.
wp() { $DC run --rm -T wpcli wp --path=/var/www/html "$@"; }

case "${1:-up}" in
  stop)
    $DC down
    echo "Stopped. Your data is preserved. Run ./setup.sh to bring it back."
    exit 0
    ;;
  reset)
    read -r -p "This DELETES the site database and files. Type 'yes' to confirm: " ok
    [[ "$ok" == "yes" ]] || { echo "Aborted."; exit 1; }
    $DC down -v
    echo "Wiped. Run ./setup.sh for a clean install."
    exit 0
    ;;
  seed)
    $DC up -d db wordpress
    $DC cp seed-curriculum.php wordpress:/tmp/seed-curriculum.php
    wp eval-file /tmp/seed-curriculum.php
    exit 0
    ;;
esac

echo "==> Starting database and WordPress containers..."
$DC up -d db wordpress

echo "==> Waiting for WordPress files to be ready..."
for i in $(seq 1 60); do
  if wp core version >/dev/null 2>&1; then break; fi
  sleep 2
done

if wp core is-installed >/dev/null 2>&1; then
  echo "==> WordPress is already installed. Skipping core install."
else
  echo "==> Installing WordPress..."
  wp core install \
    --url="$SITE_URL" \
    --title="$SITE_TITLE" \
    --admin_user="$ADMIN_USER" \
    --admin_password="$ADMIN_PASSWORD" \
    --admin_email="$ADMIN_EMAIL" \
    --skip-email
fi

echo "==> Setting pretty permalinks (Tutor LMS requires them)..."
wp rewrite structure '/%postname%/' >/dev/null
wp rewrite flush >/dev/null

echo "==> Installing and activating Tutor LMS (free)..."
wp plugin is-installed tutor >/dev/null 2>&1 || wp plugin install tutor
wp plugin activate tutor >/dev/null

echo "==> Seeding the adoption curriculum skeleton..."
if [[ -f seed-curriculum.php ]]; then
  # Copy the seeder into the container and run it via wp eval-file.
  $DC cp seed-curriculum.php wordpress:/tmp/seed-curriculum.php
  wp eval-file /tmp/seed-curriculum.php
else
  echo "    (seed-curriculum.php not found — skipping course seeding)"
fi

cat <<EOF

============================================================
  ✅  Your adoption-curriculum LMS is running.

  Site:   $SITE_URL
  Admin:  $SITE_URL/wp-admin
    user:     $ADMIN_USER
    password: $ADMIN_PASSWORD

  Next steps:
    1. Log in at the admin URL above.
    2. Left menu → "Tutor LMS" to see your courses.
    3. Edit the seeded course, or add lessons/quizzes.

  Stop it:   ./setup.sh stop
  Start it:  ./setup.sh
  Wipe it:   ./setup.sh reset
============================================================
EOF
