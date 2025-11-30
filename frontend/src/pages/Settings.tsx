export default function Settings() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Settings</h1>
      <div className="bg-dark-surface border border-dark-border rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">API Keys</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Shodan API Key</label>
            <input
              type="password"
              className="w-full px-4 py-2 bg-dark-bg border border-dark-border rounded-lg text-white"
              placeholder="Enter API key"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">HaveIBeenPwned API Key</label>
            <input
              type="password"
              className="w-full px-4 py-2 bg-dark-bg border border-dark-border rounded-lg text-white"
              placeholder="Enter API key"
            />
          </div>
        </div>

        <h2 className="text-xl font-semibold mb-4 mt-8">LLM Configuration</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">LLM Backend</label>
            <select className="w-full px-4 py-2 bg-dark-bg border border-dark-border rounded-lg text-white">
              <option value="ollama">Ollama (Local)</option>
              <option value="openai">OpenAI (Cloud)</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  )
}












