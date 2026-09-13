export interface User {
  id: number;
  is_bot: boolean;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
}

export interface Chat {
  id: number;
  type: string;
  title?: string;
  username?: string;
}

export interface MeResponse {
  user: {
    id: number;
    username: string;
    lang: string;
  };
  bot?: {
    id: number;
    username: string;
  };
  chats: Chat[];
}

export interface ChatSettingsData {
  chat_id: number;
  warn_limit: number;
  warn_action: string;
  ai_mode: string;
  ai_threshold: number;
  ai_model?: string;
  anonymize_events: boolean;
  data: Record<string, any>;
}

export interface AuditLog {
  id: number;
  action: string;
  user_id?: number;
  reason?: string;
  created_at: string;
}
