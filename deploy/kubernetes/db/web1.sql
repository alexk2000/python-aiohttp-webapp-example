--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.12
-- Dumped by pg_dump version 9.5.12

CREATE DATABASE web1;
CREATE USER web1 WITH ENCRYPTED PASSWORD 'web1';
GRANT ALL PRIVILEGES ON DATABASE web1 TO web1;


\c web1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: web1
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    name character varying(50)
);


ALTER TABLE public.groups OWNER TO web1;

--
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: web1
--

CREATE SEQUENCE public.groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groups_id_seq OWNER TO web1;

--
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: web1
--

ALTER SEQUENCE public.groups_id_seq OWNED BY public.groups.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: web1
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(50),
    price integer
);


ALTER TABLE public.products OWNER TO web1;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: web1
--

CREATE SEQUENCE public.products_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO web1;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: web1
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: web1
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    title character varying(50),
    description character varying(150),
    done boolean
);


ALTER TABLE public.tasks OWNER TO web1;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: web1
--

CREATE SEQUENCE public.tasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_id_seq OWNER TO web1;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: web1
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: web1
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    name character varying(50),
    password character varying(150),
    disabled boolean
);


ALTER TABLE public.users OWNER TO web1;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: web1
--

CREATE SEQUENCE public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO web1;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: web1
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: web1
--

ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: web1
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: web1
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: web1
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: web1
--

COPY public.groups (id, name) FROM stdin;
\.


--
-- Name: groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: web1
--

SELECT pg_catalog.setval('public.groups_id_seq', 1, false);


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: web1
--

COPY public.products (id, name, price) FROM stdin;
1	p1	10
2	\N	\N
3	p2	20
\.


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: web1
--

SELECT pg_catalog.setval('public.products_id_seq', 3, true);


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: web1
--

COPY public.tasks (id, title, description, done) FROM stdin;
139	ccccccc		\N
2	Learn Pythonasa	Need to find a good Python tutorial on the web	f
138	xxxxx1		\N
48	Shopping	buy some products	\N
140	aaa	wwwwwwww	\N
\.


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: web1
--

SELECT pg_catalog.setval('public.tasks_id_seq', 140, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: web1
--

COPY public.users (user_id, name, password, disabled) FROM stdin;
2	alex	asasdasda	f
3	alex	asasdasda	f
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: web1
--

SELECT pg_catalog.setval('public.users_user_id_seq', 3, true);


--
-- Name: groups_pkey; Type: CONSTRAINT; Schema: public; Owner: web1
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: products_pkey; Type: CONSTRAINT; Schema: public; Owner: web1
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: web1
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: web1
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

