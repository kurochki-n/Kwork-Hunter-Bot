import { FormEvent, useState, useEffect, memo } from 'react';
import { KeyRound, User, AlertCircle } from 'lucide-react';

// Немедленно устанавливаем базовые стили
(() => {
  // Добавляем стили напрямую в head
  const style = document.createElement('style');
  style.innerHTML = `
    html, body, #root {
      background-color: #18181b !important;
      color: white !important;
      margin: 0;
      padding: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
  `;
  document.head.prepend(style);
  
  // Принудительно устанавливаем цвет фона для body
  document.body.style.cssText = 'background-color: #18181b !important; color: white !important;';
})();

// Выносим форму в отдельный мемоизированный компонент
const LoginForm = memo(({ onSubmit, error, isLoading }: { 
  onSubmit: (login: string, password: string) => void, 
  error: string,
  isLoading: boolean 
}) => {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(login, password);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="login" className="block text-sm font-medium text-zinc-300 mb-2">
          Логин
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <User className="h-5 w-5 text-zinc-500" />
          </div>
          <input
            id="login"
            type="text"
            value={login}
            onChange={(e) => setLogin(e.target.value)}
            required
            disabled={isLoading}
            className="block w-full pl-10 pr-3 py-2 bg-zinc-700 border border-zinc-600 text-white rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 placeholder-zinc-400 disabled:opacity-50"
            placeholder="Введите логин или эл. почту"
          />
        </div>
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-zinc-300 mb-2">
          Пароль
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <KeyRound className="h-5 w-5 text-zinc-500" />
          </div>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={isLoading}
            className="block w-full pl-10 pr-3 py-2 bg-zinc-700 border border-zinc-600 text-white rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 placeholder-zinc-400 disabled:opacity-50"
            placeholder="Введите пароль"
          />
        </div>
      </div>

      {error && (
        <div className="bg-red-900/50 border-l-4 border-red-500 p-4 rounded">
          <div className="flex items-center">
            <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
            <p className="text-sm text-red-400">{error}</p>
          </div>
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-zinc-800 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? 'Загрузка...' : 'Войти'}
      </button>
    </form>
  );
});

function App() {
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const [messageId, setMessageId] = useState<string | null>(null);
  // @ts-ignore
  const [tg, setTg] = useState(window.Telegram?.WebApp);

  // Эффект для установки базовых стилей при монтировании
  useEffect(() => {
    document.documentElement.style.backgroundColor = '#18181b';
    document.body.style.backgroundColor = '#18181b';
    document.documentElement.style.color = 'white';
    document.body.style.color = 'white';
  }, []);

  useEffect(() => {
    let mounted = true;
    let retryCount = 0;
    const maxRetries = 5;

    const checkTelegramWebApp = () => {
      // @ts-ignore
      return window.Telegram?.WebApp;
    };

    const initApp = async () => {
      try {
        const webApp = checkTelegramWebApp();
        
        if (!webApp) {
          if (retryCount < maxRetries) {
            retryCount++;
            setTimeout(initApp, retryCount * 200);
            return;
          }
          console.error('Telegram WebApp not found after retries');
          if (mounted) {
            setError('Ошибка: Telegram WebApp не инициализирован');
          }
          return;
        }

        if (!mounted) return;
        
        const urlParams = new URLSearchParams(window.location.search);
        const msgId = urlParams.get('message_id');
        
        if (mounted) {
          setMessageId(msgId);
          setTg(webApp);
          setIsInitialized(true);
          
          // Инициализируем Telegram WebApp
          webApp.ready();
          webApp.expand();
          webApp.setBackgroundColor('#18181b');
          webApp.enableClosingConfirmation();
        }
      } catch (err) {
        console.error('Init error:', err);
        if (mounted) {
          setError('Ошибка инициализации приложения');
        }
      }
    };

    initApp();

    return () => {
      mounted = false;
    };
  }, []);

  const handleSubmit = async (login: string, password: string) => {
    setError('');
    setIsLoading(true);
    
    try {
      const userId = 1234567890;
      
      if (!userId) {
        setError('Ошибка: не удалось получить ID пользователя');
        return;
      }

      if (!messageId) {
        setError('Ошибка: не удалось получить ID сообщения');
        return;
      }
      
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 30000);
      
      try {
        const response = await fetch(`http://0.0.0.0:8000/auth`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            login,
            password,
            user_id: userId,
            message_id: messageId
          }),
          credentials: 'include',
          signal: controller.signal
        });
        
        clearTimeout(timeout);
        
        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries(response.headers.entries()));
        
        const responseText = await response.text();
        console.log('Response text:', responseText);
        
        if (!responseText) {
          throw new Error('Пустой ответ от сервера');
        }

        if (!response.ok) {
          const errorData = JSON.parse(responseText);
          throw new Error(errorData.message || 'Произошла ошибка при авторизации');
        }

        const data = JSON.parse(responseText);
        
        if (data.ok) {
          if (tg) {
            tg.close();
          }
        } else {
          setError(data.message || 'Произошла ошибка при авторизации');
        }
      } catch (err: unknown) {
        if (err instanceof Error) {
          if (err.name === 'AbortError') {
            setError('Превышено время ожидания ответа от сервера');
          } else {
            console.error('Fetch error:', err);
            setError(err.message || 'Произошла ошибка при запросе к серверу');
          }
        } else {
          console.error('Unknown error:', err);
          setError('Произошла неизвестная ошибка');
        }
      }
    } catch (err) {
      console.error('Auth error:', err);
      setError('Произошла ошибка... Не волнуйтесь, мы уже работаем над этим!');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isInitialized) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-zinc-900 to-stone-900 flex items-center justify-center p-4">
        <div className="text-white text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-orange-500 mx-auto mb-4"></div>
          <p>Загрузка приложения...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-900 to-stone-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-zinc-800 rounded-2xl shadow-xl p-8 border border-zinc-700">
          <div className="text-center mb-8">
            <div className="bg-orange-500/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <KeyRound className="w-8 h-8 text-orange-500" />
            </div>
            <h2 className="text-2xl font-bold text-white">Авторизация Kwork</h2>
            <p className="text-zinc-400 mt-2">Войдите в свой аккаунт</p>
          </div>

          <LoginForm onSubmit={handleSubmit} error={error} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}

export default App;