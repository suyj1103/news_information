

insert into tb_teacher (name, positional_title, profile, avatar_url, create_time, update_time, is_delete) values
('苏永杰', 'python高级讲师', '帅哥呀', '/media/avatar.jpg', now(), now(), 0);

insert into tb_course_category (name, create_time, update_time, is_delete) values
('数据分析', now(), now(), 0),
('深度学习', now(), now(), 0),
('机器学习', now(), now(), 0);

insert into tb_course (title, cover_url, video_url, duration, profile, outline, teacher_id, category_id, create_time, update_time, is_delete) values

('教学视频', 'http://jjexh7tyg2fmynaiqrd.exp.bcevod.com/mda-jjexjb4wy4mbg745/mda-jjexjb4wy4mbg745.jpg', 'http://jjexh7tyg2fmynaiqrd.exp.bcevod.com/mda-jjexjb4wy4mbg745/mda-jjexjb4wy4mbg745.m3u8', 10.5, '爬虫教学', '豆瓣爬取视频', 1, 2, now(), now(), 0),


('最喜欢的歌曲', 'http://jjexh7tyg2fmynaiqrd.exp.bcevod.com/mda-jjp0nxmzj1r39u01/mda-jjp0nxmzj1r39u01.jpg', 'http://jjexh7tyg2fmynaiqrd.exp.bcevod.com/mda-jjp0nxmzj1r39u01/mda-jjp0nxmzj1r39u01.m3u8', 9.9, 'music', '好听的欧美歌曲', 1, 1, now(), now(), 0);