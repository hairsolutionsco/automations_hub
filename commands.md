# Commands

## n8n Cloud Workflows
export $(grep -v '^#' .env | xargs) && npm run cloud:export
export $(grep -v '^#' .env | xargs) && npm run cloud:import
npm run workflows:sync

## Git
git add .
git commit -m "Update workflows"
git push