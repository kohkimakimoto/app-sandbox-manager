.PHONY:help dev dist packaging clean bindata fmt test testv testcov deps resetdeps
.DEFAULT_GOAL := help

# This is a magic code to output help message at default
# see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

dev: ## Build dev binary
	@bash -c $(CURDIR)/build/scripts/dev.sh

dist: ## Build dist binaries
	@bash -c $(CURDIR)/build/scripts/dist.sh

packaging: ## Create packages (now support RPM only)
	@bash -c $(CURDIR)/build/scripts/packaging.sh

clean: ## Clean the built binaries.
	@bash -c $(CURDIR)/build/scripts/clean.sh

bindata: ## bindata
	go-bindata -o ./res/static/bindata.go -ignore bindata.go -prefix res/static -pkg static res/static/...
	go-bindata -o ./res/views/bindata.go -ignore bindata.go -prefix res/views -pkg views res/views/...

fmt: ## Run `go fmt`
	go fmt $$(go list ./... | grep -v vendor)

test: ## Run all tests
	go test -cover $$(go list ./... | grep -v vendor)

testv: ## Run all tests with verbose outputing.
	go test -v -cover $$(go list ./... | grep -v vendor)

testcov: ## Run all tests and output coverage report
	gocov test $$(go list ./... | grep -v vendor) | gocov-html > .coverage.html && open .coverage.html

deps: ## Install dependences.
	go get -u github.com/mattn/go-bindata/...
	go get -u github.com/mitchellh/gox
	go get -u github.com/axw/gocov/gocov
	go get -u gopkg.in/matm/v1/gocov-html
	dep ensure

resetdeps: ## reset dependences.
	rm -rf Gopkg.*
	rm -rf vendor
	dep init
	dep ensure
