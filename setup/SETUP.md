# Setting up your own version of this profile

This repository powers a GitHub profile page, meaning the terminal style
card, the badges, and the live contribution graph you see on
github.com/RanaZaid26194 all come from the files in here. If you forked this
repo or downloaded it as a zip because you want the same setup on your own
profile, this guide walks through everything you need to change and run,
start to finish.

Nothing in here is required to run on your own computer if you do not want
to. Once the setup below is done and pushed to GitHub, the two GitHub
Actions workflows already in this repo take care of keeping everything
updated automatically, forever, for free.

## Step 1: name and visibility of the repository

GitHub only turns a repository into a profile page under one very specific
condition, the repository name has to match your GitHub username exactly,
and the repository has to be public. So if your username is `ali`, the
repository must be named `ali`, nothing else will work.

If you forked this repo, rename it from your repository settings page. If
you downloaded the zip instead, create a new repository with that exact
name and push this code into it.

## Step 2: let the workflows write back to your repo

Both automated workflows in `.github/workflows` end by committing their
freshly generated files back into your repository, and by default a brand
new repo does not allow that.

Go to your repository's Settings tab, then Actions, then General, scroll
down to Workflow permissions, and switch it to Read and write permissions.
Save that change. Without this one setting, both workflows will run
successfully but fail on their very last step when they try to push.

## Step 3: make the card your own

Open `generate_profile.py` and change the following:

* `USERNAME` near the top, set it to your own GitHub username.
* The `INFO` list a little further down, this is every line of text shown
  in the right hand panel of the card. Each row is a label, a value, and a
  colour name. Replace the role, education, focus, stack, and project rows
  with your own, and update the GitHub, LinkedIn and email lines under
  `~/reach` at the bottom.
* The `THEMES` dictionary if you want different colours, though the
  defaults already match GitHub's own dark and light themes closely, so
  most people can leave this alone.

You do not need to install anything to run this file. It only uses Python's
own standard library, so `python generate_profile.py` works right away on
any machine with Python 3 installed, and it is exactly what the workflow
runs for you automatically every day regardless.

## Step 4: make the badges your own

Open `generate_badges.py` and edit the `BADGES` list near the bottom. Each
entry has a key, a label, a url, and an icon. Change every url to point to
your own LinkedIn, GitHub, email, and project links.

If you want to add a brand new badge for a project that is not already
listed, copy one of the existing dictionaries in `BADGES`, give it a new
key and label, and either point `icon` at a traced svg path for that
project's logo or leave it as `mono=` with a single capital letter as a
placeholder until you have a proper icon ready.

This script also needs nothing installed beyond Python itself.

## Step 5: the ascii portrait, optional

The little ascii art person on the left of the card comes from
`portrait.txt`, which is produced by `setup/photo_to_ascii.py`. This part
is entirely optional, if you skip it the card just shows a small
placeholder message instead of a portrait, and everything else still
works normally.

If you do want your own photo turned into ascii art, install the few
extra packages this one script needs, since these are not required
anywhere else in the project:

```
pip install pillow numpy rembg onnxruntime
```

Then run it, pointing at a clear photo of yourself, ideally one where you
are reasonably centred and well lit:

```
python setup/photo_to_ascii.py your_photo.jpg
```

This writes `portrait.txt` into the root of the repository. Commit that
file, and `generate_profile.py` will pick it up automatically the next
time it runs.

## Step 6: the live contribution graph

Open `.github/workflows/update-contrib-terminal.yml` and change the
`GH_USERNAME` value under the Generate live contribution panel step to
your own username. That is the only edit required here, the workflow
already provides a token automatically through
`secrets.GITHUB_TOKEN`, so you do not need to create or paste in any
token yourself.

If you would like to preview this one on your own machine before pushing,
you will need Node.js 20 or newer installed, nothing else, since the
script only uses Node's built in modules. Set two environment variables
and run it directly:

```
export GH_USERNAME=your-username
export GH_TOKEN=a-github-personal-access-token
node scripts/generate-contrib-terminal.js
```

A personal access token with basic public read access is enough for this,
you can create one from your GitHub account's Developer settings page.

## Step 7: update the README itself

Open `README.md` and change every link that still points to Rana Zaid's
LinkedIn, GitHub, email and project pages so they point to yours instead.
The image references themselves, `dark.svg`, `light.svg`, the badge files,
and the contribution panel files, can stay exactly as they are, since
those filenames do not need to change, only what is written inside them
does, which the scripts above already take care of.

## Step 8: push and let the workflows take over

Commit everything and push to your `main` branch. From here, two things
happen on their own with no further effort from you:

* `.github/workflows/profile.yml` rebuilds `dark.svg`, `light.svg`, and
  every badge once a day, and also immediately whenever you edit
  `generate_profile.py`, `generate_badges.py`, or `portrait.txt`.
* `.github/workflows/update-contrib-terminal.yml` rebuilds the
  contribution graph once a day, and also on every push to `main`.

If you do not want to wait for the daily schedule the first time, open the
Actions tab on your repository, choose either workflow from the list on
the left, and use the Run workflow button to trigger it immediately by
hand.

Once both workflows have run at least once, visit
`github.com/your-username` and your new profile page should be live.

## A quick note on what actually needs installing

To be completely clear about dependencies, since it is easy to assume
more setup is required than actually is: the two workflows that run every
day, the profile card and the contribution graph, need nothing installed
beyond what GitHub Actions already sets up for you automatically, which is
just a plain Python and a plain Node.js environment. The only extra
packages anywhere in this whole project are the four listed in step 5,
and those are only ever needed if you choose to generate your own ascii
portrait from a photo on your own machine.

## One last thing

If this setup saved you some time, drop a star on the original repository or a follow on GitHub !
