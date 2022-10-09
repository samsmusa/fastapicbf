create table if not exists auth_group
(
    id     int auto_increment
        primary key,
    name   varchar(150) not null,
    active tinyint(1)   not null,
    constraint name
        unique (name)
);

create table if not exists authentication_user
(
    id                bigint auto_increment
        primary key,
    password          varchar(128) not null,
    last_login        datetime(6)  null,
    is_superuser      tinyint(1)   not null,
    username          varchar(150) not null,
    first_name        varchar(150) not null,
    last_name         varchar(150) not null,
    is_staff          tinyint(1)   not null,
    is_active         tinyint(1)   not null,
    date_joined       datetime(6)  not null,
    created_at        datetime(6)  not null,
    updated_at        datetime(6)  not null,
    email_verified_at datetime(6)  not null,
    email             varchar(254) not null,
    phone             varchar(40)  null,
    profile_image     varchar(100) null,
    gender            varchar(2)   null,
    birth_date        date         null,
    age               int          null,
    location          varchar(200) null,
    country_code      varchar(3)   null,
    country           varchar(255) null,
    city              varchar(255) null,
    address           varchar(255) null,
    bio               longtext     null,
    constraint email
        unique (email),
    constraint username
        unique (username)
);

create table if not exists authentication_user_groups
(
    id       bigint auto_increment
        primary key,
    user_id  bigint not null,
    group_id int    not null,
    constraint authentication_user_groups_user_id_group_id_8af031ac_uniq
        unique (user_id, group_id),
    constraint authentication_user__user_id_30868577_fk_authentic
        foreign key (user_id) references authentication_user (id),
    constraint authentication_user_groups_group_id_6b5c44b7_fk_auth_group_id
        foreign key (group_id) references auth_group (id)
);

create table if not exists django_content_type
(
    id        int auto_increment
        primary key,
    app_label varchar(100) not null,
    model     varchar(100) not null,
    constraint django_content_type_app_label_model_76bd3d3b_uniq
        unique (app_label, model)
);

create table if not exists auth_permission
(
    id              int auto_increment
        primary key,
    name            varchar(255) not null,
    content_type_id int          not null,
    codename        varchar(100) not null,
    constraint auth_permission_content_type_id_codename_01ab375a_uniq
        unique (content_type_id, codename),
    constraint auth_permission_content_type_id_2f476e4b_fk_django_co
        foreign key (content_type_id) references django_content_type (id)
);

create table if not exists auth_group_permissions
(
    id            bigint auto_increment
        primary key,
    group_id      int not null,
    permission_id int not null,
    constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
        unique (group_id, permission_id),
    constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
        foreign key (permission_id) references auth_permission (id),
    constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
        foreign key (group_id) references auth_group (id)
);

create table if not exists authentication_user_user_permissions
(
    id            bigint auto_increment
        primary key,
    user_id       bigint not null,
    permission_id int    not null,
    constraint authentication_user_user_user_id_permission_id_ec51b09f_uniq
        unique (user_id, permission_id),
    constraint authentication_user__permission_id_ea6be19a_fk_auth_perm
        foreign key (permission_id) references auth_permission (id),
    constraint authentication_user__user_id_736ebf7e_fk_authentic
        foreign key (user_id) references authentication_user (id)
);

create table if not exists django_admin_log
(
    id              int auto_increment
        primary key,
    action_time     datetime(6)       not null,
    object_id       longtext          null,
    object_repr     varchar(200)      not null,
    action_flag     smallint unsigned not null,
    change_message  longtext          not null,
    content_type_id int               null,
    user_id         bigint            not null,
    constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
        foreign key (content_type_id) references django_content_type (id),
    constraint django_admin_log_user_id_c564eba6_fk_authentication_user_id
        foreign key (user_id) references authentication_user (id),
    check (`action_flag` >= 0)
);

create table if not exists django_migrations
(
    id      bigint auto_increment
        primary key,
    app     varchar(255) not null,
    name    varchar(255) not null,
    applied datetime(6)  not null
);

create table if not exists django_session
(
    session_key  varchar(40) not null
        primary key,
    session_data longtext    not null,
    expire_date  datetime(6) not null
);

create index django_session_expire_date_a5c62663
    on django_session (expire_date);

create table if not exists filter_job
(
    id          bigint auto_increment
        primary key,
    title       varchar(255) null,
    description longtext     not null
);

create table if not exists filter_jobprofile
(
    id     bigint auto_increment
        primary key,
    skills longtext not null,
    job_id bigint   not null,
    constraint filter_jobprofile_job_id_592c30c5_fk_filter_job_id
        foreign key (job_id) references filter_job (id)
);

create table if not exists filter_skilltype
(
    id   bigint auto_increment
        primary key,
    type varchar(500) null
);

create table if not exists filter_skill
(
    id      bigint auto_increment
        primary key,
    skill   varchar(100) null,
    type_id bigint       not null,
    constraint filter_skill_type_id_3907bfe3_fk_filter_skilltype_id
        foreign key (type_id) references filter_skilltype (id)
);

create table if not exists filter_job_skill
(
    id       bigint auto_increment
        primary key,
    job_id   bigint not null,
    skill_id bigint not null,
    constraint filter_job_skill_job_id_skill_id_01bfd827_uniq
        unique (job_id, skill_id),
    constraint filter_job_skill_job_id_5e4c173e_fk_filter_job_id
        foreign key (job_id) references filter_job (id),
    constraint filter_job_skill_skill_id_7cd1efee_fk_filter_skill_id
        foreign key (skill_id) references filter_skill (id)
);

create table if not exists filter_youth
(
    id              bigint auto_increment
        primary key,
    name            varchar(50)  null,
    education_label varchar(100) not null,
    education_field varchar(100) not null
);

create table if not exists filter_youth_skill
(
    id       bigint auto_increment
        primary key,
    youth_id bigint not null,
    skill_id bigint not null,
    constraint filter_youth_skill_youth_id_skill_id_be4fae76_uniq
        unique (youth_id, skill_id),
    constraint filter_youth_skill_skill_id_287d5d5d_fk_filter_skill_id
        foreign key (skill_id) references filter_skill (id),
    constraint filter_youth_skill_youth_id_60b6c021_fk_filter_youth_id
        foreign key (youth_id) references filter_youth (id)
);

create table if not exists filter_youthprofile
(
    id       bigint auto_increment
        primary key,
    skills   longtext not null,
    youth_id bigint   not null,
    constraint filter_youthprofile_youth_id_74a19028_fk_filter_youth_id
        foreign key (youth_id) references filter_youth (id)
);

