# Contributing

I'm glad you consider contributing the discord bot. See the steps
below as to how exactly submit your contribution.

## 1. Forking the repository

Start out by forking the repository from 
https://github.com/kenokrieger/gaussbot.

## 2. Clone the repository

Next up you can clone the github repository you just created to 
your local pc.

````commandline
git clone https://github.com/YOUR_USERNAME/gaussbot YOUR_LOCAL_DIRECTORY
````

to keep your forked repository up to date also add the original repository
to your remotes.

````commandline
git remote add upstream https://github.com/kenokrieger/gaussbot
````
## 3. Make a new branch

Create a new branch to develop your feature on.

```commandline
git checkout -b YOUR_FEATURE_NAME
```

## 4. Start developing your feature

Hack, hack, hack

## 5. Get the recent changes

Merge the newest changes from the original repository into your forked
repository

````commandline
git fetch upstream
git merge upstream/master master
````

## 6. Implement your feature

Merge your feature branch with the main branch and resolve conflicts

````commandline
git checkout main
git merge YOUR_FEATURE_NAME
````

Push your changes to your repository

````commandline
git push origin main
````

## 7. Pull request

Finally, you can issue a pull request to implement your feature in
the main build.
