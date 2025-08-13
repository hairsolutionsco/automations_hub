# Commands

## n8n
export $(grep -v '^#' .env.n8n | xargs) && n8n
npm run n8n:import
npm run n8n:export

## Git
git add .
git commit -m "msg"
git push