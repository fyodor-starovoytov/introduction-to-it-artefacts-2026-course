#!/bin/sh
# setup_template.sh — Lab 3C starting point: prepare a fresh machine for this course.
# Fill in NAME and EMAIL, then run:  sh setup_template.sh
# Safe to run twice: every step checks before it acts.
NAME="Your Name"
EMAIL="you@example.com"

echo "== tools =="
for tool in git python3 code ssh-keygen; do
  if command -v "$tool" >/dev/null 2>&1; then echo "  ok      $tool"; else echo "  MISSING $tool  <- install it, then run me again"; fi
done

echo "== git identity =="
git config --global user.name "$NAME"
git config --global user.email "$EMAIL"
git config --global init.defaultBranch main
echo "  $(git config --global user.name) <$(git config --global user.email)>"

echo "== key pair =="
if [ -f "$HOME/.ssh/id_ed25519.pub" ]; then
  echo "  already have one"
else
  ssh-keygen -t ed25519 -C "$EMAIL" -f "$HOME/.ssh/id_ed25519" -N "" >/dev/null
  echo "  made a new key pair"
fi
echo "  paste this line into your account's SSH keys page:"
echo
cat "$HOME/.ssh/id_ed25519.pub"
echo
echo "== python =="
python3 --version
echo "done. Next: ssh -T git@gitlab.jyu.fi:kataka/isep1000-introduction-to-it-artefacts-2026-27.git"
