--
-- PostgreSQL database dump
--

\restrict 3eWDumSAx4DENTbrQa0pap0eUnj2zaofP5MuivM4gxMDinrm2PeoLuXRMSgUsTP

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: completed; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.completed (
    ku_id character varying(50) NOT NULL,
    course_code character varying(50) NOT NULL,
    year integer NOT NULL,
    grade integer NOT NULL
);


ALTER TABLE public.completed OWNER TO postgres;

--
-- Name: course; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.course (
    course_code character varying(50) NOT NULL,
    course_name character varying(200) NOT NULL,
    course_credits double precision NOT NULL
);


ALTER TABLE public.course OWNER TO postgres;

--
-- Name: grade_distribution; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grade_distribution (
    course_code character varying(50) NOT NULL,
    grade_value integer NOT NULL,
    year integer NOT NULL,
    count integer NOT NULL
);


ALTER TABLE public.grade_distribution OWNER TO postgres;

--
-- Name: prediction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prediction (
    request_id character varying(12) NOT NULL,
    course_code character varying(50) NOT NULL,
    predicted_grade integer NOT NULL,
    z_score double precision
);


ALTER TABLE public.prediction OWNER TO postgres;

--
-- Name: prediction_request; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prediction_request (
    request_id character varying(12) NOT NULL,
    student_id character varying(50) NOT NULL,
    request_date timestamp without time zone DEFAULT now()
);


ALTER TABLE public.prediction_request OWNER TO postgres;

--
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    ku_id character varying(50) NOT NULL,
    major character varying(100)
);


ALTER TABLE public.student OWNER TO postgres;

--
-- Data for Name: completed; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.completed (ku_id, course_code, year, grade) FROM stdin;
eqs232	NDAB15003E	2025	12
\.


--
-- Data for Name: course; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.course (course_code, course_name, course_credits) FROM stdin;
NDAA04011E	Algoritmer og datastrukturer	7.5
NDAA09025E	IT-sikkerhed	7.5
NDAB15003E	Interaktionsdesign	7.5
NDAB15011E	Softwareudvikling	15
NDAB16005E	Computersystemer	15
NDAB16006E	Implementering af programmeringssprog	7.5
NDAB16012E	Modelling and Analysis of Data	7.5
NDAB18002E	Matematisk analyse og sandsynlighedsteori for dataloger	7.5
NDAB21010E	Databases and Information Systems	7.5
NMAB15002E	Lineær algebra i datalogi	7.5
NNDB19000E	Datalogiens videnskabsteori	7.5
\.


--
-- Data for Name: grade_distribution; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.grade_distribution (course_code, grade_value, year, count) FROM stdin;
NDAA04011E	-3	2023	9
NDAA04011E	0	2023	30
NDAA04011E	2	2023	62
NDAA04011E	4	2023	42
NDAA04011E	7	2023	44
NDAA04011E	10	2023	28
NDAA04011E	12	2023	18
NDAA09025E	-3	2023	1
NDAA09025E	0	2023	3
NDAA09025E	2	2023	11
NDAA09025E	4	2023	13
NDAA09025E	7	2023	17
NDAA09025E	10	2023	10
NDAA09025E	12	2023	2
NDAB15003E	-3	2023	0
NDAB15003E	0	2023	3
NDAB15003E	2	2023	11
NDAB15003E	4	2023	38
NDAB15003E	7	2023	69
NDAB15003E	10	2023	38
NDAB15003E	12	2023	5
NDAB15011E	-3	2023	0
NDAB15011E	0	2023	5
NDAB15011E	2	2023	4
NDAB15011E	4	2023	19
NDAB15011E	7	2023	34
NDAB15011E	10	2023	32
NDAB15011E	12	2023	35
NDAB16005E	-3	2023	1
NDAB16005E	0	2023	24
NDAB16005E	2	2023	14
NDAB16005E	4	2023	13
NDAB16005E	7	2023	35
NDAB16005E	10	2023	19
NDAB16005E	12	2023	9
NDAB16006E	-3	2023	4
NDAB16006E	0	2023	18
NDAB16006E	2	2023	18
NDAB16006E	4	2023	15
NDAB16006E	7	2023	15
NDAB16006E	10	2023	9
NDAB16006E	12	2023	7
NDAB16012E	-3	2023	0
NDAB16012E	0	2023	5
NDAB16012E	2	2023	9
NDAB16012E	4	2023	8
NDAB16012E	7	2023	23
NDAB16012E	10	2023	35
NDAB16012E	12	2023	31
NDAB18002E	-3	2023	0
NDAB18002E	0	2023	33
NDAB18002E	2	2023	8
NDAB18002E	4	2023	20
NDAB18002E	7	2023	20
NDAB18002E	10	2023	11
NDAB18002E	12	2023	9
NDAB21010E	-3	2023	6
NDAB21010E	0	2023	46
NDAB21010E	2	2023	46
NDAB21010E	4	2023	35
NDAB21010E	7	2023	55
NDAB21010E	10	2023	24
NDAB21010E	12	2023	11
NMAB15002E	-3	2023	34
NMAB15002E	0	2023	18
NMAB15002E	2	2023	30
NMAB15002E	4	2023	68
NMAB15002E	7	2023	71
NMAB15002E	10	2023	47
NMAB15002E	12	2023	29
NNDB19000E	-3	2023	0
NNDB19000E	0	2023	6
NNDB19000E	2	2023	16
NNDB19000E	4	2023	49
NNDB19000E	7	2023	61
NNDB19000E	10	2023	51
NNDB19000E	12	2023	8
\.


--
-- Data for Name: prediction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prediction (request_id, course_code, predicted_grade, z_score) FROM stdin;
6a016a	NDAB15011E	12	1.9511157234902101
ee0071	NDAB21010E	12	1.9511157234902101
\.


--
-- Data for Name: prediction_request; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prediction_request (request_id, student_id, request_date) FROM stdin;
6a016a	eqs232	2026-05-21 12:55:48.364761
ee0071	eqs232	2026-05-21 12:58:04.063542
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student (ku_id, major) FROM stdin;
eqs232	\N
\.


--
-- Name: completed completed_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.completed
    ADD CONSTRAINT completed_pkey PRIMARY KEY (ku_id, course_code, year);


--
-- Name: course course_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_pkey PRIMARY KEY (course_code);


--
-- Name: grade_distribution grade_distribution_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade_distribution
    ADD CONSTRAINT grade_distribution_pkey PRIMARY KEY (course_code, grade_value, year);


--
-- Name: prediction prediction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prediction
    ADD CONSTRAINT prediction_pkey PRIMARY KEY (request_id, course_code);


--
-- Name: prediction_request prediction_request_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prediction_request
    ADD CONSTRAINT prediction_request_pkey PRIMARY KEY (request_id);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (ku_id);


--
-- Name: completed uq_completed_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.completed
    ADD CONSTRAINT uq_completed_unique UNIQUE (ku_id, course_code, year);


--
-- Name: prediction uq_request_course; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prediction
    ADD CONSTRAINT uq_request_course UNIQUE (request_id, course_code);


--
-- Name: completed completed_course_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.completed
    ADD CONSTRAINT completed_course_code_fkey FOREIGN KEY (course_code) REFERENCES public.course(course_code);


--
-- Name: completed completed_ku_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.completed
    ADD CONSTRAINT completed_ku_id_fkey FOREIGN KEY (ku_id) REFERENCES public.student(ku_id);


--
-- Name: grade_distribution grade_distribution_course_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grade_distribution
    ADD CONSTRAINT grade_distribution_course_code_fkey FOREIGN KEY (course_code) REFERENCES public.course(course_code);


--
-- Name: prediction prediction_course_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prediction
    ADD CONSTRAINT prediction_course_code_fkey FOREIGN KEY (course_code) REFERENCES public.course(course_code);


--
-- Name: prediction prediction_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prediction
    ADD CONSTRAINT prediction_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.prediction_request(request_id);


--
-- Name: prediction_request prediction_request_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prediction_request
    ADD CONSTRAINT prediction_request_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(ku_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

\unrestrict 3eWDumSAx4DENTbrQa0pap0eUnj2zaofP5MuivM4gxMDinrm2PeoLuXRMSgUsTP

