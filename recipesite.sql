--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.my_recipes DROP CONSTRAINT my_recipes_user_id_fkey;
ALTER TABLE ONLY public.bookmarks DROP CONSTRAINT bookmarks_user_id_fkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_user_name_key;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
ALTER TABLE ONLY public.my_recipes DROP CONSTRAINT my_recipes_pkey;
ALTER TABLE ONLY public.bookmarks DROP CONSTRAINT bookmarks_pkey;
ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
ALTER TABLE public.my_recipes ALTER COLUMN recipe_id DROP DEFAULT;
ALTER TABLE public.bookmarks ALTER COLUMN bookmark_id DROP DEFAULT;
DROP SEQUENCE public.users_user_id_seq;
DROP TABLE public.users;
DROP SEQUENCE public.my_recipes_recipe_id_seq;
DROP TABLE public.my_recipes;
DROP SEQUENCE public.bookmarks_bookmark_id_seq;
DROP TABLE public.bookmarks;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: bookmarks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bookmarks (
    bookmark_id integer NOT NULL,
    user_id integer NOT NULL,
    api_recipe_id integer NOT NULL
);


--
-- Name: bookmarks_bookmark_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bookmarks_bookmark_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bookmarks_bookmark_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bookmarks_bookmark_id_seq OWNED BY public.bookmarks.bookmark_id;


--
-- Name: my_recipes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.my_recipes (
    recipe_id integer NOT NULL,
    recipe_name character varying(100) NOT NULL,
    ingredients character varying(5000) NOT NULL,
    directions character varying(5000) NOT NULL,
    ratings integer,
    prep_time character varying(25) NOT NULL,
    cook_time character varying(25) NOT NULL,
    cuisine character varying(25) NOT NULL,
    notes character varying(25),
    user_id integer NOT NULL
);


--
-- Name: my_recipes_recipe_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.my_recipes_recipe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: my_recipes_recipe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.my_recipes_recipe_id_seq OWNED BY public.my_recipes.recipe_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_name character varying(25) NOT NULL,
    email character varying(25) NOT NULL,
    password character varying(25) NOT NULL
);


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: bookmarks bookmark_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks ALTER COLUMN bookmark_id SET DEFAULT nextval('public.bookmarks_bookmark_id_seq'::regclass);


--
-- Name: my_recipes recipe_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.my_recipes ALTER COLUMN recipe_id SET DEFAULT nextval('public.my_recipes_recipe_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: bookmarks; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.bookmarks (bookmark_id, user_id, api_recipe_id) FROM stdin;
1	4	707788
7	5	1061311
8	5	1064614
9	6	1061311
10	6	1064614
13	3	589956
14	3	852462
16	2	986940
17	7	44053
18	7	1059776
19	8	986374
20	8	1115920
23	4	986940
24	4	985185
25	3	985185
26	3	991414
27	4	957264
\.


--
-- Data for Name: my_recipes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.my_recipes (recipe_id, recipe_name, ingredients, directions, ratings, prep_time, cook_time, cuisine, notes, user_id) FROM stdin;
10	Sinangag	Garlic\r\nRice\r\nSalt	Saute Garlic. Add Rice. Season with Salt.	\N	15 min	15 min	Filipino	\N	4
11	Scrambled Eggs	3 eggs\r\nbutter	Heat butter, pour in beaten eggs	\N	15 min	15 min	American	\N	6
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, user_name, email, password) FROM stdin;
1	Anna Marie	anna@anna.com	annapw
2	Adam	adam@adam.com	adampw
3	Avery Alfredo	avery@avery.com	averypw
4	Ariel Melody	ariel@ariel.com	arielpw
5	Emma	emma@emma.com	emmapw
6	Briceida	briceida@briceida.com	briceidapw
7	Andie	andie@andie.com	andiepw
8	Tiffany	tiffany@tiffany.com	tiffanypw
9	Simon	simon@simon.com	simonpw
\.


--
-- Name: bookmarks_bookmark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.bookmarks_bookmark_id_seq', 37, true);


--
-- Name: my_recipes_recipe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.my_recipes_recipe_id_seq', 11, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 9, true);


--
-- Name: bookmarks bookmarks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks
    ADD CONSTRAINT bookmarks_pkey PRIMARY KEY (bookmark_id);


--
-- Name: my_recipes my_recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.my_recipes
    ADD CONSTRAINT my_recipes_pkey PRIMARY KEY (recipe_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_user_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_name_key UNIQUE (user_name);


--
-- Name: bookmarks bookmarks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks
    ADD CONSTRAINT bookmarks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: my_recipes my_recipes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.my_recipes
    ADD CONSTRAINT my_recipes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

