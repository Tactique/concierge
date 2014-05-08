concierge
=========

Your personal concierge for repository management

usage
-----

Set your $ROOTIQUE environment variable to /path/to/concierge/repos/

	export ROOTIQUE=/home/bob/concierge/repos

To start using concierge to clone and setup the repos use (clone, setup)

	./concierge bootstrap

To sync all of your repos (git pull --rebase)

	./concierge sync

To reset all repos (clear, clone, setup)

    ./concierge reset

To clear all repos (rm)

	./concierge clear

To clone but not setup (git clone)

	./concierge clone

To setup with cloned repos (./setup.sh)

	./concierge setup

To see the status of all repos (git status)

	./concierge status

To run all runable repos (./run.sh)

	./concierge run

To stop all running repos (pkill)

	./concierge kill
