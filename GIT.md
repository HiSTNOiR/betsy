# GIT

What's the active branch? `git branch` (\* marks active one)

What's branches are there? `git branch`

What needs doing? `git status`

Create a new branch for a new feature:

```bash
git checkout -b branch_name_here
git add .
git commit -m 'message'
git push -u origin branch_name_here
```

When ready to merge with main:

```bash
git checkout main
git pull
git merge branch_name_here
git push
```

Delete branch after merging with main:

```bash
git branch -d branch_name_here # deletes it locally
git push origin --delete branch_name_here # deletes it on GitHub/remote server
```

Conflicts?

```bash
git add resolved_files_here
git commit -m 'thing here'
```

Updating my local copy with any main branch changes after I've already been doing shit on my end:

```bash
# While in my own branch
git pull --rebase origin main
# gets changes from main and applies them to my local code
# replays my changes on top of the new code so I don't lose anything
```
