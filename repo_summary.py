from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/create_readme/<owner>/<repo>')
def create_readme(owner, repo):
  # Use the GitHub API to get a list of all the files in the repository
  response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents',
                          headers={'Authorization': 'Bearer YOUR_ACCESS_TOKEN'})
  
  # Create a list of the file contents
  file_contents = [file.content for file in response.json()]
  
  # Use the ChatGPT API to summarize the list of file contents
  response = requests.post('https://api.openai.com/v1/summarize',
                           headers={'Content-Type': 'application/json',
                                    'Authorization': 'Bearer YOUR_API_KEY'},
                           json={'model': 'text-davinci-002',
                                 'prompt': '\n\n'.join(file_contents)})
  
  # Get the summary generated by the ChatGPT API
  summary = response.json()['data']['summary']
  
  # Use the GitHub API to create a new file with the summary
  response = requests.put(f'https://api.github.com/repos/{owner}/{repo}/contents/AutoREADME.md',
                          headers={'Content-Type': 'application/json',
                                   'Authorization': 'Bearer YOUR_ACCESS_TOKEN'},
                          json={'message': 'Adding summary to repository generated by Open AI ChatGPT',
                                'content': summary})

  # Return a success message
  return 'AutoReadme file successfully created!'

if __name__ == '__main__':
  app.run()
