"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ArrowLeft, Save, Key } from "lucide-react";

type Provider = "openrouter" | "openai" | "grok" | "gemini";

interface Settings {
  provider: Provider;
  apiKey: string;
}

const providerInfo = {
  openrouter: {
    name: "OpenRouter",
    description: "Access multiple LLM models through OpenRouter",
    defaultModel: "nvidia/nemotron-nano-12b-v2-vl:free",
    baseUrl: "https://openrouter.ai/api/v1",
  },
  openai: {
    name: "OpenAI",
    description: "Use OpenAI's GPT models",
    defaultModel: "gpt-4o-mini",
    baseUrl: "https://api.openai.com/v1",
  },
  grok: {
    name: "Grok (xAI)",
    description: "Use xAI's Grok models",
    defaultModel: "grok-2-1212",
    baseUrl: "https://api.x.ai/v1",
  },
  gemini: {
    name: "Google Gemini",
    description: "Use Google's Gemini models",
    defaultModel: "gemini-2.0-flash",
    baseUrl: "https://generativelanguage.googleapis.com/v1beta",
  },
};

export default function SettingsPage() {
  const router = useRouter();
  const [settings, setSettings] = useState<Settings>({
    provider: "openrouter",
    apiKey: "",
  });
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("llm_settings");
    if (stored) {
      setSettings(JSON.parse(stored));
    }
  }, []);

  const handleSave = () => {
    localStorage.setItem("llm_settings", JSON.stringify(settings));
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-2xl mx-auto">
        <Button
          variant="ghost"
          onClick={() => router.push("/")}
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Home
        </Button>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Key className="h-5 w-5" />
              LLM Settings
            </CardTitle>
            <CardDescription>
              Configure your LLM provider and API key
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="provider">Provider</Label>
              <Select
                value={settings.provider}
                onValueChange={(value: Provider) =>
                  setSettings({ ...settings, provider: value })
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select provider" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(providerInfo).map(([key, info]) => (
                    <SelectItem key={key} value={key}>
                      {info.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-sm text-muted-foreground">
                {providerInfo[settings.provider].description}
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="apiKey">API Key</Label>
              <Input
                id="apiKey"
                type="password"
                placeholder="Enter your API key"
                value={settings.apiKey}
                onChange={(e) =>
                  setSettings({ ...settings, apiKey: e.target.value })
                }
              />
              <p className="text-sm text-muted-foreground">
                Your API key is stored locally and never sent to our servers
              </p>
            </div>

            <div className="p-4 rounded-lg bg-muted">
              <h4 className="font-medium mb-2">Selected Provider Info</h4>
              <div className="text-sm text-muted-foreground space-y-1">
                <p><strong>Provider:</strong> {providerInfo[settings.provider].name}</p>
                <p><strong>Default Model:</strong> {providerInfo[settings.provider].defaultModel}</p>
                <p><strong>API Base:</strong> {providerInfo[settings.provider].baseUrl}</p>
              </div>
            </div>

            <Button onClick={handleSave} className="w-full">
              <Save className="mr-2 h-4 w-4" />
              {saved ? "Saved!" : "Save Settings"}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
