# -*- coding: utf-8 -*-

""""""


from Util.AboutDB import DbConnection



def get_db_con(host, user_name, password, db_name, port = 3306):
    """
    :param host:
    :param user_name:
    :param password:
    :param db_name:
    :param port:
    :return:
    """
    return DbConnection.DbConnection(host, user_name, password, db_name)


def get_root_path(taxon_id, db_con):
    """

    :param taxon_id:
    :param db_con:
    :return:
    """
    path = []
    path.append(taxon_id)
    parent_id = taxon_id
    while parent_id != 0:
        sql = "SELECT parent_id FROM ncbi_taxa_node WHERE taxon_id = %s" % (str(parent_id))
        db_con.execute_query(sql)
        if not db_con.has_query():
            print("=== query error ===")
        else:
            res = db_con.get_res()
            # print(res)
            # print(len(res))
            parent_id = int(res[0][0])
            path.append(parent_id)
    return path


def get_all_leaf_node(taxon_id, total_leaf_nodes, db_con):
    """

    :param taxon_id:
    :param total_leaf_nodes:
    :param db_con:
    :return:
    """
    sql = "SELECT taxon_id FROM taxon_tree WHERE parent_id = %s" % (taxon_id)
    db_con.execute_query(sql)
    if not db_con.has_query():
        print("=== query error ===")
    else:
        res = db_con.get_res()
        print("=== res ===", res)
        if len(res) == 0:
            total_leaf_nodes.append(int(taxon_id))
        else:
            for each in res:
                get_all_leaf_node(each[0], total_leaf_nodes, db_con)


def get_rank(taxon_id, db_con):
    """

    :param taxon_id:
    :param db_con:
    :return:
    """
    sql = "SELECT rank FROM ncbi_taxa_node WHERE taxon_id = %s" % (taxon_id)
    db_con.execute_query(sql)
    return db_con.get_res()[0][0]


def add_parent_info(taxon_id, parent_id, meta_con):
    """

    :param taxon_id:
    :param parent_id:
    :param meta_con:
    :return:
    """
    sql = "SELECT taxon_id FROM taxon_tree WHERE taxon_id = %s" % (taxon_id)
    meta_con.execute_query(sql)
    if not meta_con.has_query():
        print("=== meta con query error")
    else:
        res = meta_con.get_res()
        if len(res) == 0:
            sql = "INSERT INTO taxon_tree (taxon_id, parent_id) VALUE (%s,%s)" % (taxon_id, parent_id)
            meta_con.execute_query(sql)
            if not meta_con.has_query():
                print("=== parent info insert error ===")


def add_root_path(root_path_list, meta_con):
    """

    :param root_path_list:
    :param meta_con:
    :return:
    """
    for k, v in enumerate(root_path_list):
        if v != 0:
            add_parent_info(v, root_path_list[k + 1], meta_con)


def get_all_organism_taxon_id(meta_con, start, offset):
    """

    :param meta_con:
    :param start:
    :param offset:
    :return:
    """
    sql = "SELECT species_taxonomy_id FROM organism LIMIT %s,%s" % (start, offset)
    meta_con.execute_query(sql)
    if meta_con.has_query():
        return meta_con.get_res()
    else:
        print("=== meta con get genomes taxon id error ===")


if __name__ == '__main__':
    ncbi_con = get_db_con("localhost", 'root', 'root', 'ncbi_taxonomy')
    meta_con = get_db_con("localhost", 'root', 'root', 'ensemble_metadata')
    meta_con.set_autocommit()
    total_leaf_nodes = []
    get_all_leaf_node(9989, total_leaf_nodes, meta_con)
    print(total_leaf_nodes)