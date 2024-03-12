/* Assistants DB Tables - version of the 10th of January 2024 
Almost everything is handled on Open AI side (hosting of the knowledge + conversation history)
*/

CREATE TABLE IF NOT EXISTS public.clients (
    id SERIAL PRIMARY KEY, 
    client_name VARCHAR(55) UNIQUE NOT NULL, -- For internal use. Use 'client company' to refer to name visible to the client.
    client_company VARCHAR(55),
    client_domain VARCHAR(55),
    client_email VARCHAR(120),
    client_pss VARCHAR(300),
    client_logo VARCHAR(200),
    total_file_size_in_mb NUMERIC(10, 2),
    last_connection TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    username VARCHAR(55) NOT NULL,
    first_name VARCHAR(35),
    last_name VARCHAR(35),
    user_email VARCHAR(100),
    user_pss VARCHAR(300),
    lang VARCHAR(10) DEFAULT 'eng', 
    ip TEXT,  -- we will store all the user ips in a table format
    -- For granular management you can add: user_role VARCHAR(7) CHECK (role IN ('Admin', 'User', 'Manager'))
    fraudulent BOOLEAN DEFAULT FALSE,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.library (
	id VARCHAR(100) PRIMARY KEY, --the one obtained from Open AI (will be unique)
    client_id INTEGER NOT NULL,
	file_name VARCHAR(200) NOT NULL,
	date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

/* Assistant informations */
CREATE TABLE IF NOT EXISTS public.assistants (
	id VARCHAR(100) PRIMARY KEY, --the one obtained from Open AI (will be unique)
    client_id INTEGER NOT NULL,
	assistant_name VARCHAR(100) NOT NULL,
	instructions TEXT NOT NULL,
	gpt_model VARCHAR(100) NOT NULL, -- Once we have the names, we simply add CHECK (gpt_model IN ('Name1', 'Name2', 'Name3'))
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS public.assistants_users (
	id SERIAL PRIMARY KEY,
	assistant_id VARCHAR(100) NOT NULL,
	user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

/* Threads to the assistant */
CREATE TABLE IF NOT EXISTS public.threads (
	id VARCHAR(100) PRIMARY KEY, --the one obtained from Open AI (will be unique)
	assistant_id VARCHAR(100) NOT NULL,
    user_id INTEGER NOT NULL,
    first_words VARCHAR(50) NOT NULL,
	date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

/* Assistant files */
-- already natively available https://platform.openai.com/docs/api-reference/assistants/listAssistantFiles