export type LocaleDict = Record<string, string>;
export type Locales = 'en' | 'ru' | 'uk';

export const LOCALES: Record<Locales, LocaleDict> = {
  en: {
    'sec.rbac': 'Roles & Access',
    'sec.rbac.desc': 'Panel access management',

    'rbac.title': 'Roles & Access',
    'rbac_fetch_error': 'Error loading moderators',
    'rbac_add_error': 'Error adding moderator',
    'rbac_remove_error': 'Error removing moderator',
    'rbac_remove_confirm': 'Remove moderator?',
    'rbac_username_placeholder': 'username or ID',
    'rbac_moderators_list': 'MODERATORS',
    'rbac_no_moderators': 'No moderators found.',

    'common.noMedia': 'No media',
    'common.mediaAttached': 'Media attached',
    'common.removeMedia': 'Remove media',

    'pay.title': 'Choose Payment Method',
    'pay.subtitle': 'How would you like to pay for RedQueen Pro?',
    'pay.stars.title': 'Telegram Stars',
    'pay.stars.desc': 'Fast and native payment',
    'pay.crypto.title': 'Crypto Pay',
    'pay.crypto.desc': 'TON, USDT, BTC, ETH',

    'tips.captcha': 'Enable Captcha to block bots.',
    'tips.antiflood': 'Enable Anti-Flood to reduce spam.',
    'tips.ai': 'Enable AI moderation for smart filtering.',
    'tips.raid': 'Anti-Raid is off, your group is vulnerable.',
    'tips.filters': 'Set up filters to block unwanted content.',
    'tips.quarantine': 'You have pending messages in Quarantine.',

    'act.warn': 'Warn',
    'act.ban': 'Ban',
    'act.unban': 'Unban',
    'act.mute': 'Mute',
    'act.unmute': 'Unmute',
    'act.kick': 'Kick',
    'dur.1h': '1 Hour',
    'dur.8h': '8 Hours',
    'dur.1d': '1 Day',
    'dur.7d': '7 Days',
    'cat.spam': 'Spam',
    'cat.scam': 'Scam',
    'cat.toxicity': 'Toxicity',
    'cat.nsfw': 'NSFW',
    'cat.flood': 'Flood',
    'cat.ok': 'OK',
    'media.photo': 'Photos',
    'media.video': 'Videos',
    'media.document': 'Files',
    'media.animation': 'GIFs',
    'media.voice': 'Voice Msgs',
    'media.video_note': 'Video Notes',
    'media.sticker': 'Stickers',

    'ob.btn.pro': 'Unlock PRO for {stars}⭐️',
    'pro.price': '{stars}⭐️ / month',
    'pro.until': 'PRO until {date}',
    'members.confirm': 'Are you sure you want to {action} {user}?',
    'members.messages': 'Messages: {count}',

    'ai.maxPerMinute': 'Max Requests / Min',
    'ai.mode': 'AI Action Mode',
    'ai.mode.autoban': 'Auto-ban',
    'ai.mode.off': 'Off',
    'ai.mode.quarantine': 'Quarantine',
    'ai.perCategory': 'Per-category Overrides',
    'ai.threshold': 'Confidence Threshold',
    'antiflood.action': 'Action',
    'antiflood.banSeconds': 'Ban Duration',
    'antiflood.enabled': 'Enable Anti-Flood',
    'antiflood.limit': 'Message Limit',
    'antiflood.muteSeconds': 'Mute Duration',
    'antiflood.window': 'Time Window (sec)',
    'audit.empty': 'No audit events found.',
    'audit.export': 'Export CSV',
    'audit.title': 'Audit Log',
    'captcha.enabled': 'Enable Captcha',
    'captcha.mode': 'Captcha Mode',
    'captcha.mode.button': 'Simple Button',
    'captcha.mode.math': 'Math Equation',
    'captcha.timeout': 'Timeout (sec)',
    'common.loading': 'Loading...',
    'common.minutes': 'm',
    'common.saved': 'Saved',
    'common.saving': 'Saving...',
    'common.seconds': 's',
    'dur.perm': 'Permanent',
    'exempt.add': 'Add Exception',
    'exempt.empty': 'No exceptions yet.',
    'filters.forwards': 'Block Forwards',
    'filters.links': 'Block Links',
    'filters.media': 'Block Media',
    'filters.mentions': 'Block Mentions',
    'filters.words': 'Bad Words (Comma separated)',
    'filters.wordsPlaceholder': 'e.g. scam, crypto...',
    'members.banned': 'Banned',
    'members.duration': 'Duration',
    'members.empty': 'No members found.',
    'members.muted': 'Muted',
    'members.reason': 'Reason',
    'members.search': 'Search...',
    'modes.night': 'Night Mode',
    'modes.nightRange': 'Night Time Range',
    'modes.silent': 'Silent Mode',
    'modes.silentDesc': 'Delete all new messages',
    'modes.slow': 'Slow Mode',
    'modes.slowDesc': 'Limit messages per user',
    'nav.audit': 'Audit',
    'nav.stats': 'Stats',
    'ob.btn.continue': 'Continue',
    'ob.btn.finish': 'Finish',
    'ob.btn.skip': 'Skip',
    'ob.card.1': 'AI Core',
    'ob.card.1.sub': 'Context-aware moderation',
    'ob.card.2': 'Protection',
    'ob.card.2.block': 'Blocks',
    'ob.card.2.block.sub': 'Spam & Links',
    'ob.card.2.sub': 'Anti-Raid & Captcha',
    'ob.desc.1': 'Configure AI intelligence',
    'ob.desc.2': 'Basic security layers',
    'ob.desc.3': 'You are all set!',
    'ob.pro.unlocked': 'PRO Unlocked',
    'ob.title.1': 'Step 1',
    'ob.title.2': 'Step 2',
    'ob.title.3': 'Complete',
    'pro.active': 'PRO Active',
    'pro.autobanNote': 'PRO required for Auto-ban',
    'pro.badge': 'PRO',
    'pro.opening': 'Opening billing...',
    'pro.pitch': 'Get full autonomy with RedQueen PRO',
    'pro.raidNote': 'Advanced Anti-Raid is PRO only',
    'pro.upgrade': 'Upgrade to PRO',
    'quar.approve': 'Approve',
    'quar.ban': 'Ban',
    'quar.confidence': 'Confidence',
    'quar.empty': 'Quarantine is empty',
    'quar.from': 'From',
    'quar.rule': 'Rule',
    'quar.title': 'Quarantine',
    'raid.enabled': 'Enable Anti-Raid',
    'raid.lock': 'Lockdown',
    'raid.locked': 'Group is locked down!',
    'raid.threshold': 'Joins Threshold',
    'raid.unlock': 'Unlock',
    'raid.window': 'Time Window (sec)',
    'sec.exempt': 'Exceptions',
    'sec.exempt.desc': 'Users ignoring filters',
    'start.btn.channel': 'Add to Channel',
    'start.btn.group': 'Add to Group',
    'start.desc': 'Select where to add RedQueen',
    'start.title': 'Get Started',
    'stats.actions': 'Actions',
    'stats.categories': 'Categories',
    'stats.last14': 'Last 14 days',
    'stats.members': 'Members',
    'stats.pending': 'Pending',
    'stats.proPitch': 'Get more insights with PRO',
    'stats.proTitle': 'PRO Analytics',
    'stats.title': 'Statistics',
    'stats.total': 'Total',
    'tips.allGood': 'Everything looks good!',
    'tips.title': 'Tips',
    'warns.action': 'Action on Limit',
    'warns.banDuration': 'Ban Duration',
    'warns.limit': 'Max Warns',
    'warns.muteDuration': 'Mute Duration',
    'wn.btn.back': 'Back',
    'wn.btn.finish': 'Finish',
    'wn.btn.next': 'Next',
    'wn.desc.1': 'Desc 1',
    'wn.desc.2': 'Desc 2',
    'wn.desc.3': 'Desc 3',
    'wn.desc.4': 'Desc 4',
    'wn.title.1': 'Title 1',
    'wn.title.2': 'Title 2',
    'wn.title.3': 'Title 3',
    'wn.title.4': 'Title 4',

    'common.error': 'Connection error',
    'common.retry': 'Retry',
    'common.save': 'Save',
    'common.cancel': 'Cancel',
    'common.uploading': 'Uploading...',
    'common.upload': 'Upload File',
    
    'app.title': 'RedQueen',
    'app.subtitle': 'Select a chat to manage',
    'chats.subtitle': 'YOUR CHATS',
    'chats.group': 'Group',
    'chats.supergroup': 'Supergroup',
    'chats.channel': 'Channel',
    
    'nav.dashboard': 'Overview',
    'nav.members': 'Members',
    'nav.quarantine': 'Quarantine',
    
    'dash.chatLang': 'Chat notification language',
    'dash.protection': 'Protection',
    'dash.content': 'Content & flood',
    'dash.intelligence': 'Intelligence',
    'dash.enabled': 'Active',
    'dash.disabled': 'Off',
    'dash.privacy': 'Live feed anonymization',
    'dash.privacy.desc': 'Partially hide chat/user names on the public live feed',
    
    'sec.captcha': 'Captcha',
    'sec.captcha.desc': 'Verify newcomers before they can speak',
    'sec.antiflood': 'Anti-Flood',
    'sec.antiflood.desc': 'Dampen message bursts',
    'sec.filters': 'Filters',
    'sec.filters.desc': 'Block links, forwards, bad words',
    'sec.modes': 'Restrictions',
    'sec.modes.desc': 'Night mode, read-only, slow mode',
    'sec.welcome': 'Welcome Messages',
    'sec.welcome.desc': 'Greet new members automatically',
    'welcome.text': 'Welcome Message',
    'welcome.text.ph': 'Welcome, {name}! Enjoy the {chat} chat.',
    'welcome.desc': 'Configure a message to greet new members when they join the group. Use {name} and {chat} variables.',
    'welcome.media': 'Welcome Media',
    'welcome.media.uploaded': 'Media uploaded successfully',
    'welcome.media.change': 'Change Media',
    'welcome.media.upload': 'Upload Media',
    'sec.webhooks': 'Webhooks',
    'webhooks.desc': 'Receive HTTP POST requests for moderation events like bans or warnings.',
    'webhooks.url': 'Webhook URL',
    'sec.triggers': 'Auto-Replies',
    'sec.triggers.desc': 'Custom command triggers',
    'triggers.desc': 'Configure the bot to reply automatically to specific phrases or commands.',
    'triggers.add': 'Add New Trigger',
    'triggers.phrase': 'Phrase or Command',
    'triggers.phrase.ph': 'e.g. /rules or price',
    'triggers.reply': 'Reply Text',
    'triggers.reply.ph': 'The bot will send this...',
    'triggers.regex': 'Use Regex',
    'triggers.btn.add': 'Add Trigger',
    'triggers.active': 'Active Triggers',
    'triggers.empty': 'No triggers found.',
    'triggers.btn.delete': 'Delete',

    'sec.raid': 'Anti-Raid',
    'sec.raid.desc': 'Lockdown on massive join spikes',
    'sec.warns': 'Warns',
    'sec.warns.desc': 'Strike system for violations',
    'sec.ai': 'AI Core',
    'sec.ai.desc': 'Context-aware toxicity & spam detection',
    
    'sec.autocomment': 'Auto-Comment',
    'sec.autocomment.desc': 'First comment in discussions',
    'sec.autocomment.enable': 'Enable feature',
    'sec.autocomment.enable.desc': 'Post comment under new channel posts',
    'sec.autocomment.text': 'Comment Text',
    'sec.autocomment.text.ph': 'Text (Markdown & HTML supported)...',
    'sec.autocomment.media': 'Media File (Optional)',
    'sec.autocomment.media.desc': 'If a media file is uploaded, the text will be used as a caption.',

    'action.ban': 'Ban',
    'action.mute': 'Mute',
    'action.kick': 'Kick',
    
    'stats.empty': 'No data yet',
    
    // Landing Page
    'landing.nav.features': 'Features',
    'landing.nav.live': 'Live Feed',
    'landing.nav.pricing': 'Pricing',
    'landing.nav.login': 'Add to Telegram',
    
    'landing.hero.badge': 'Next-Gen Autonomous AI Moderation',
    'landing.hero.title1': 'Keep your communities ',
    'landing.hero.title_safe': 'safe',
    'landing.hero.title2': ' and ',
    'landing.hero.title_clean': 'clean',
    'landing.hero.desc': 'RedQueen is an advanced AI moderator that analyzes context, detects toxicity, bans scammers, and protects your Telegram groups 24/7 with zero configuration.',
    'landing.hero.cta': 'Protect Your Group',
    'landing.hero.demo': 'View Live Action',
    
    'landing.stats.title': 'Global Impact',
    'landing.stats.chats': 'Protected Communities',
    'landing.stats.actions': 'Actions Taken',
    'landing.stats.ai': 'AI Verdicts',
    
    'landing.features.title': 'Why Choose RedQueen?',
    'landing.features.desc': 'Military-grade protection meets elegant Telegram integration.',
    
    'landing.feat1.title': 'Context-Aware AI',
    'landing.feat1.desc': 'Our neural networks understand sarcasm, context, and intent. No more false bans for regular words.',
    'landing.feat2.title': 'Smart Anti-Raid',
    'landing.feat2.desc': 'Automatically detects botnets and join spikes, locking down the group before spam can be sent.',
    'landing.feat3.title': 'Seamless Mini App',
    'landing.feat3.desc': 'Manage settings, view audit logs, and handle quarantine directly inside Telegram without clunky commands.',
    'landing.feat4.title': 'Advanced Filters',
    'landing.feat4.desc': 'Granular control over media, links, forwards, and specific words with regex support.',
    
    'landing.live.title': 'RedQueen in Action',
    'landing.live.desc': 'Real-time feed of moderation actions happening right now across the network.',
    
    'landing.pricing.title': 'Transparent Pricing',
    'landing.pricing.desc': 'Pay only for the AI power you need. Basic protection is always free.',
    'landing.price.free': 'Free',
    'landing.price.free.desc': 'Essential tools for any group',
    'landing.price.pro': 'Pro',
    'landing.price.pro.desc': 'Full AI autonomy for serious communities',
    'landing.price.month': '/month',
    
    'landing.plan.feat.basic': 'Basic Captcha & Anti-flood',
    'landing.plan.feat.filters': 'Standard Filters',
    'landing.plan.feat.warns': 'Warning System',
    'landing.plan.feat.ai': 'Deep AI Context Analysis',
    'landing.plan.feat.raid': 'Advanced Anti-Raid',
    'landing.plan.feat.priority': 'Priority Processing',
    'landing.plan.cta.free': 'Get Started',
    'landing.plan.cta.pro': 'Upgrade Now',
    
    'landing.footer.rights': 'All rights reserved.',

    'settings.crossChatTitle': 'Cross-Chat Blacklist',
    'settings.crossChatDesc': 'Instantly ban users who were banned in your other chats.',
    'settings.aiProvider': 'AI Provider',
    'settings.aiProvider.local': 'Local (Ollama)',
    'settings.aiProvider.openai': 'OpenAI',
    'settings.aiProvider.gemini': 'Gemini',
    'settings.aiProvider.claude': 'Claude',
    'settings.apiKey': 'API Key',
    'settings.apiKeySaved': '(Saved)',
    'settings.enterApiKey': 'Enter API Key',
    'settings.model': 'Model',
    'settings.modelPlaceholder': 'e.g. gpt-4o-mini',
    'settings.removeMedia': 'Remove Media',
    
    'live.feedTitle': 'LIVE MODERATION FEED',
    'live.waiting': 'Waiting for live events...',
    'live.banned': 'Banned',
    'live.warned': 'Warned',
    'live.muted': 'Muted',
    'live.kicked': 'Kicked',
    'live.unbanned': 'Unbanned',
    'live.inChat': 'in {chat}',
    
    'error.title': 'Oops, something broke!',
    'error.desc': 'A critical error occurred in the interface. Please reload the application.',
    'error.reload': 'Reload App',
    
    'triggers.regexBadge': 'REGEX'
  },
  
  ru: {








    
    
    
    



    
    
    // Landing Page
    
    
    
    
    
    
    
    

    
    
    
  },
  
  uk: {







    
    
    
    



    
    
    // Landing Page
    
    
    
    
    
    
    
    

    
    
    
  }
}

export function resolveLang(code: string): Locales {
  const c = (code || 'en').toLowerCase().slice(0, 2)
  if (LOCALES[c]) return c
  return 'en'
}
