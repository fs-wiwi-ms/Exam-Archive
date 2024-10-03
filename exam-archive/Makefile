# Directories
SEED_DIR = seed
SCRIPT_DIR = ./scripts

# Targets
.PHONY: loadseed createseed help default

# Default behavior if no target is specified
default: help

# Load the seed data from a specified seed file
loadseed:
	@if [ -f $(SCRIPT_DIR)/load_seed.sh ]; then \
		$(SCRIPT_DIR)/load_seed.sh; \
	else \
		echo "Error: Script 'load_seed.sh' not found in $(SCRIPT_DIR)"; \
		exit 1; \
	fi

# Call the shell script to create a new seed file
createseed:
	@if [ -f $(SCRIPT_DIR)/create_seed.sh ]; then \
		$(SCRIPT_DIR)/create_seed.sh; \
	else \
		echo "Error: Script 'create_seed.sh' not found in $(SCRIPT_DIR)"; \
		exit 1; \
	fi


# Help: List available commands
help:
	@echo "Available commands:"
	@echo "  loadseed          Load seed data from the seed file"
	@echo "  createseed        Create a new seed file with automatic numbering and naming"
