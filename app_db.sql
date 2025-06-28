-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 28, 2025 at 01:25 PM
-- Server version: 10.6.22-MariaDB-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `app_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `diagrams`
--

CREATE TABLE `diagrams` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `template_id` int(11) NOT NULL,
  `source_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `vars` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `diagrams`
--

INSERT INTO `diagrams` (`id`, `name`, `template_id`, `source_id`, `group_id`, `vars`) VALUES
(2, 'Доля зачетов', 4, 5, 2, '{\"Идент\" : \"ID\", \"Количество\" : \"@counter@\", \"Категория\" : \"@result@\"}\r\n'),
(3, 'РЕЗУЛЬТАТЫ', 1, 1, 2, '{\"id\" : \"ID\", \"grade\" : \"@grade@\", \"name\" : \"@name@\"}\r\n'),
(4, 'ТЕСТ_ДИАГ', 1, 0, 0, '{\"Идентификатор\" : \"ID\", \"Баллы\" : \"@grade@\", \"Тест\" : \"@name@\"}\n'),
(5, 'Ghbvth', 5, 1, 1, '[object Object]'),
(6, 'Ex1', 5, 2, 2, '{\"name\":\"@counter@\",\"grade\":\"@result@\",\"id\":\"ID\"}'),
(7, 'ПРОВЕРКА', 4, 7, 2, '{\"grade\":\"@grade@\",\"name\":\"@name@\",\"id\":\"ID\"}'),
(8, 'ЗАЧЕТЫ', 5, 5, 2, '{\"Количество\":\"@counter@\",\"Категория\":\"@result@\",\"Идент\":\"ID\"}');

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE `groups` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `privileged` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `groups`
--

INSERT INTO `groups` (`id`, `name`, `privileged`) VALUES
(0, 'Пользователь', 0),
(1, 'Админ', 1),
(2, 'Студенты', 0);

-- --------------------------------------------------------

--
-- Table structure for table `plots`
--

CREATE TABLE `plots` (
  `id` int(11) NOT NULL,
  `feature` tinytext NOT NULL,
  `code` text NOT NULL,
  `name` tinytext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `plots`
--

INSERT INTO `plots` (`id`, `feature`, `code`, `name`) VALUES
(2, 'a_bar_2', 'global quizzes, visibility\r\nquizzes = list(set(df[\'name\'].tolist()))\r\n#create array of plots as it will be in memory on client\r\nbars = []\r\nfor i in quizzes:\r\n	plot_df = df[df[\'name\'] == i]\r\n	plot_df[\'questionid\'] = plot_df[\'questionid\'].apply(str)\r\n	bar_trace = go.Bar(x=plot_df.questionid, y=plot_df.average, name=i, text = plot_df.questionsummary, marker=dict(color = plot_df[\'average\'].tolist(), colorscale=\'rdbu\'), visible=False)\r\n	bars.append(bar_trace)\r\nbars[0].visible = True\r\nfig = go.Figure(data=bars)     \r\nvisibility = [[i == j for j in range(len(quizzes))] for i in range(len(quizzes))]\r\nbutton = [\r\n		{\r\n		\"label\": quizzes[i],\r\n		\"method\": \"update\",\r\n		\"args\": [\r\n			{\"visible\": visibility[i]},\r\n  			{\"title\": quizzes[i]}\r\n			]\r\n		} for i in range(len(quizzes))]\r\nfig.update_layout(updatemenus=[dict(active=0, buttons=button, yanchor=\"top\", showactive=True, xanchor=\"left\", y=1.1)], xaxis_title=\'Вопрос\', yaxis_title=\'Балл\')', 'Статистика заданий'),
(3, 'a_bar_1', 'global quizzes, visibility\r\nquizzes = list(set(df[\'name\'].tolist()))\r\nboxes = []\r\nfor i in quizzes:\r\n	plot_df = df[df[\'name\'] == i]\r\n	box_trace = go.Box(x=plot_df.group_name, y=plot_df.grade, name=i, visible=False)\r\n	boxes.append(box_trace)\r\nboxes[0].visible = True\r\nfig = go.Figure(data=boxes)\r\nvisibility = [[i == j for j in range(len(quizzes))] for i in range(len(quizzes))]\r\nbutton = [{\r\n	\"label\": quizzes[i],\r\n	\"method\": \"update\",\r\n	\"args\": [\r\n		{\"visible\": visibility[i]},\r\n		{\"title\": quizzes[i]}\r\n		]}\r\n	for i in range(len(quizzes))]\r\n\r\nfig.update_layout(updatemenus=[dict(active=0, buttons=button, yanchor=\"top\", showactive=True, xanchor=\"left\", y=1.1)], xaxis_title=\'Группа\', yaxis_title=\'Оценка в %\')', 'Статистика групп'),
(4, 'bar_1', 'df[\"pass_t\"] = [\"Сдано\" if gr >= 70 else \"Не сдано\" for gr in df[\"@grade@\"]]\r\nfig = px.bar(df, x=\"@name@\", y=\"@grade@\", color=\"pass_t\", labels={\"pass_t\":\"Статус\"}, color_discrete_map={\"Не сдано\": \"red\", \"Сдано\": \"green\"})\r\nfig.update_layout(xaxis_title=\'Тест\', yaxis_title=\'Оценка в %\', hovermode=\"x\", minreducedheight=300, legend=dict(orientation=\"h\", yanchor=\"bottom\", y=1.02, xanchor=\"right\",x=1),)\r\nfig.update_traces(hovertemplate=None)', 'Результаты тестов'),
(5, 'pie_1', 'fig = px.pie(df, values=\"@counter@\", names=\"@result@\", title=\"Доля зачетов по тестам\")', 'Доля зачетов'),
(6, 'bar_2', 'fig = px.bar(df, y=\"name\", x=\"grade\", color=\"type\", barmode=\'group\', text=\"name\", labels={\"type\":\"Роль\"})\r\nfig.update_layout(xaxis_title=\'Баллы\', yaxis_title=None, hovermode=\"y\", minreducedheight=295)\r\nfig.update_layout(legend=dict(orientation=\"h\", yanchor=\"bottom\", y=1.02, xanchor=\"right\",x=1))\r\nfig.update_layout(yaxis = {\'title\': \'y-axis\', \'visible\': False, \'showticklabels\': False})\r\nfig.update_traces(hovertemplate=(\'<b>%{x:.2f}</b><extra></extra>\'), textposition=\"inside\")', 'Сравнение результатов'),
(13, 'pie_2', '#available objects: fig, px, go\n#to use your own variables define it as globa\nprint(\"bye bye bye\")', 'Диаг_рез'),
(14, 'srgfv', '#available objects: fig, px, go\r\n#to use your own variables define it as global\r\n', 'DAF');

-- --------------------------------------------------------

--
-- Table structure for table `sources`
--

CREATE TABLE `sources` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `type` tinyint(1) NOT NULL,
  `path` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sources`
--

INSERT INTO `sources` (`id`, `name`, `type`, `path`) VALUES
(2, 'ТЕСТ_SQL', 1, 'localhost&moodle_dev&vis_read@\nSELECT `mdl_user`.`id`, `mdl_quiz_grades`.`quiz`, `mdl_quiz`.`name`, `mdl_quiz`.`course`, `mdl_quiz_grades`.`grade` / `mdl_quiz`.`grade` * 100 AS grade\nFROM `mdl_quiz_grades`\nJOIN `mdl_user`\nON `mdl_quiz_grades`.`userid` = `mdl_user`.`id`\nJOIN `mdl_quiz`\nON `mdl_quiz_grades`.`quiz` = `mdl_quiz`.`id`'),
(3, 'запросы', 0, 'uploads/queries.csv'),
(4, 'moodle_оценки', 0, 'uploads/mdl_quiz_grades.csv'),
(5, 'nhfj', 0, 'uploads/результаты.csv'),
(7, 'Тесты1', 0, 'uploads/mdl_user_query_res.csv'),
(8, 'Результаты moodle', 1, 'localhost&moodle_dev&vis_read@SELECT `mdl_user`.`id`, `mdl_quiz_grades`.`quiz`, `mdl_quiz`.`name`, `mdl_quiz_grades`.`grade`, `mdl_groups`.`name` AS `group_name`\nFROM `mdl_quiz_grades`\nJOIN `mdl_user`\nON `mdl_quiz_grades`.`userid` = `mdl_user`.`id`\nJOIN `mdl_quiz`\nON `mdl_quiz_grades`.`quiz` = `mdl_quiz`.`id`\nJOIN `mdl_groups_members`\nON `mdl_groups_members`.`userid` = `mdl_user`.`id`\nJOIN `mdl_groups`\nON `mdl_groups_members`.`groupid` = `mdl_groups`.`id`\nORDER BY `mdl_user`.`id`  '),
(9, 'Диаг_рез', 1, 'localhost&moodle_dev&vis_read@SELECT \r\n\r\n'),
(10, 'SQL на lessons', 1, 'localhost&moodle_dev&vis_read@select * from `mdl_grade_grades` grades where grades.itemid in (select items.id from `mdl_grade_items` items WHERE items.itemmodule = \"lesson\")  ');

-- --------------------------------------------------------

--
-- Table structure for table `sources_u`
--

CREATE TABLE `sources_u` (
  `id` int(11) DEFAULT NULL,
  `name` text NOT NULL,
  `type` tinyint(1) NOT NULL,
  `path` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sources_u`
--

INSERT INTO `sources_u` (`id`, `name`, `type`, `path`) VALUES
(NULL, 'ТЕСТ_CSV', 0, 'uploads/test.csv'),
(NULL, 'ТЕСТ_SQL', 1, 'localhost&moodle_dev&vis_read@\r\nSELECT `mdl_user`.`id`, `mdl_quiz_grades`.`quiz`, `mdl_quiz`.`name`, `mdl_quiz`.`course`, `mdl_quiz_grades`.`grade` / `mdl_quiz`.`grade` * 100 AS grade\r\nFROM `mdl_quiz_grades`\r\nJOIN `mdl_user`\r\nON `mdl_quiz_grades`.`userid` = `mdl_user`.`id`\r\nJOIN `mdl_quiz`\r\nON `mdl_quiz_grades`.`quiz` = `mdl_quiz`.`id`\r\n'),
(NULL, 'CSV с результатами', 0, 'uploads/результаты.csv');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `group_id`, `password`) VALUES
(1, 1, '12345'),
(6, 2, ''),
(100, 2, ''),
(104, 2, ''),
(240, 0, ''),
(2401, 0, '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `diagrams`
--
ALTER TABLE `diagrams`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `plots`
--
ALTER TABLE `plots`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `feature` (`feature`) USING HASH,
  ADD KEY `id` (`id`);

--
-- Indexes for table `sources`
--
ALTER TABLE `sources`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `diagrams`
--
ALTER TABLE `diagrams`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `plots`
--
ALTER TABLE `plots`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `sources`
--
ALTER TABLE `sources`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
