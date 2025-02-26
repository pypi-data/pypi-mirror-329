import os
import re
import sys
import pandas as pd
import subprocess
import warnings

# supress deprecation warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=DeprecationWarning)
    from Bio.Blast import NCBIXML
    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

# from Bio.Blast import NCBIWWW
# from Bio.Blast.Applications import NcbiblastnCommandline
# from Bio.Blast.Applications import NcbimakeblastdbCommandline


class Blaster():
    def __init__(self, inputfile, database, output, threads, minid=90, mincov=60, blast_type='blastn'):
        self.inputfile = os.path.abspath(inputfile)
        self.database = database
        self.minid = int(minid)
        self.mincov = int(mincov)
        self.temp_output = os.path.join(os.path.abspath(output), 'temp.xml')
        self.threads = threads
        self.blast_type = blast_type

    def biopython_blast(self):
        hsp_results = {}
        # biopython no longer support the NcbiblastnCommandline
        # replace NcbiblastnCommandline using subprocess with blastn

        # cline = NcbiblastnCommandline(query=self.inputfile, db=self.database, dust='no',
        #                               evalue=1E-20, out=self.temp_output, outfmt=5,
        #                               perc_identity=self.minid, max_target_seqs=50000,
        #                               num_threads=self.threads)
        # print(cline)
        # print(self.temp_output)
        if self.blast_type == 'blastn':
            cline = [self.blast_type, '-query', self.inputfile, '-db', self.database,
                     '-dust', 'no', '-evalue', '1E-20', '-out', self.temp_output,
                     '-outfmt', '5', '-perc_identity', str(
                         self.minid), '-max_target_seqs', '50000',
                     '-num_threads', str(self.threads)]
        elif self.blast_type == 'blastx':
            cline = [self.blast_type, '-query', self.inputfile, '-db', self.database,
                     '-evalue', '1E-20', '-out', self.temp_output,
                     '-outfmt', '5', '-max_target_seqs', '50000',
                     '-num_threads', str(self.threads)]
        else:
            print('Wrong blast type, exit ...')
            sys.exit(1)

        # stdout, stderr = cline()
        # print(cline)

        # Run the command using subprocess
        result = subprocess.run(
            cline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Capture the output and error
        stdout = result.stdout
        stderr = result.stderr

        # Print or handle the output and error as needed
        # print(stdout)
        if stderr:
            print(f"Error: {stderr}")

        result_handler = open(self.temp_output)

        blast_records = NCBIXML.parse(result_handler)
        df_final = pd.DataFrame()

        # solve local variable referenced before assignment
        loop_check = 0
        save = 0

        for blast_record in blast_records:

            # if blast_record.alignments:
            #     print("QUERY: %s" % blast_record.query)
            # else:
            #     for alignment in blast_record.alignments:
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    strand = 0

                    query_name = blast_record.query
                    # print(query_name)
                    # print(alignment.title)
                    target_gene = alignment.title.partition(' ')[2]

                    # Get gene name and accession number from target_gene
                    gene = target_gene.split('___')[0]
                    accession = target_gene.split('___')[2]
                    classes = target_gene.split('___')[3]  # 增加种类
                    # print(classes)
                    # print(target_gene)
                    sbjct_length = alignment.length  # The length of matched gene
                    # print(sbjct_length)
                    sbjct_start = hsp.sbjct_start
                    sbjct_end = hsp.sbjct_end
                    gaps = hsp.gaps  # gaps of alignment
                    query_string = str(hsp.query)  # Get the query string
                    sbjct_string = str(hsp.sbjct)
                    identities_length = hsp.identities  # Number of indentity bases
                    # contig_name = query.replace(">", "")
                    query_start = hsp.query_start
                    query_end = hsp.query_end
                    # length of query sequence
                    query_length = len(query_string)

                    # calculate identities
                    perc_ident = (int(identities_length)
                                  / float(query_length) * 100)
                    IDENTITY = "%.2f" % perc_ident
                    # print("Identities: %s " % perc_ident)

                    # coverage = ((int(query_length) - int(gaps))
                    #             / float(sbjct_length))
                    # print(coverage)

                    perc_coverage = (((int(query_length) - int(gaps))
                                      / float(sbjct_length)) * 100)
                    COVERAGE = "%.2f" % perc_coverage

                    # print("Coverage: %s " % perc_coverage)

                    # cal_score is later used to select the best hit
                    cal_score = perc_ident * perc_coverage

                    # Calculate if the hit is on minus strand
                    if sbjct_start > sbjct_end:
                        temp = sbjct_start
                        sbjct_start = sbjct_end
                        sbjct_end = temp
                        strand = 1
                        query_string = str(
                            Seq(str(query_string)).reverse_complement())
                        sbjct_string = str(
                            Seq(str(sbjct_string)).reverse_complement())

                    if strand == 0:
                        strand_direction = '+'
                    else:
                        strand_direction = '-'

                    if perc_coverage >= self.mincov and perc_ident >= self.minid:
                        loop_check += 1
                        hit_id = "%s:%s_%s:%s" % (
                            query_name, query_start, query_end, target_gene)
                        # print(hit_id)
                        # hit_id = query_name
                        # print(hit_id)
                        best_result = {
                            'FILE': os.path.basename(self.inputfile),
                            'SEQUENCE': query_name,
                            'GENE': gene,
                            'START': query_start,
                            'END': query_end,
                            'SBJSTART': sbjct_start,
                            'SBJEND': sbjct_end,
                            'STRAND': strand_direction,
                            # 'COVERAGE':
                            'GAPS': gaps,
                            "%COVERAGE": COVERAGE,
                            "%IDENTITY": IDENTITY,
                            # 'DATABASE':
                            'ACCESSION': accession,
                            'CLASSES': classes,
                            'QUERY_SEQ': query_string,
                            'SBJCT_SEQ': sbjct_string,
                            'cal_score': cal_score,
                            'remove': 0
                            # 'PRODUCT': target_gene,
                            # 'RESISTANCE': target_gene
                        }
                        # print(best_result)

                        # solve local variable referenced before assignment
                        if best_result:
                            save = 1

                            if hsp_results:
                                tmp_results = hsp_results
                                save, hsp_results = Blaster.filter_results(
                                    save, best_result, tmp_results)

                    if save == 1:
                        hsp_results[hit_id] = best_result
        # close file handler, then remove temp file
        result_handler.close()
        os.remove(self.temp_output)
        # print(self.inputfile)
        if loop_check == 0:
            df = pd.DataFrame(columns=['FILE', 'SEQUENCE', 'GENE', 'START', 'END', 'SBJSTART',
                                       'SBJEND', 'STRAND', 'GAPS', '%COVERAGE', '%IDENTITY', 'ACCESSION', 'CLASSES'])
        else:
            df = Blaster.resultdict2df(hsp_results)
        # print(hsp_results)
        return df, hsp_results

    def biopython_blastx(self):
        hsp_results = {}
        # biopython no longer support the NcbiblastnCommandline
        # replace NcbiblastnCommandline using subprocess with blastn

        # cline = NcbiblastnCommandline(query=self.inputfile, db=self.database, dust='no',
        #                               evalue=1E-20, out=self.temp_output, outfmt=5,
        #                               perc_identity=self.minid, max_target_seqs=50000,
        #                               num_threads=self.threads)
        # print(cline)
        # print(self.temp_output)

        cline = [self.blast_type, '-query', self.inputfile, '-db', self.database,
                 '-evalue', '1E-20', '-out', self.temp_output,
                 '-outfmt', '5', '-max_target_seqs', '50000',
                 '-num_threads', str(self.threads)]

        # stdout, stderr = cline()

        # Run the command using subprocess
        result = subprocess.run(
            cline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Capture the output and error
        stdout = result.stdout
        stderr = result.stderr

        # Print or handle the output and error as needed
        # print(stdout)
        if stderr:
            print(f"Error: {stderr}")

        result_handler = open(self.temp_output)

        blast_records = NCBIXML.parse(result_handler)
        df_final = pd.DataFrame()

        # solve local variable referenced before assignment
        loop_check = 0
        save = 0

        for blast_record in blast_records:

            # if blast_record.alignments:
            #     print("QUERY: %s" % blast_record.query)
            # else:
            #     for alignment in blast_record.alignments:
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    strand = 0

                    query_name = blast_record.query
                    # print(query_name)
                    # print(alignment.title)
                    target_gene = alignment.title.partition(' ')[2]

                    # Get gene name and accession number from target_gene
                    gene = target_gene.split('___')[0]
                    accession = target_gene.split('___')[2]
                    classes = target_gene.split('___')[3]  # 增加种类
                    # print(classes)
                    # print(target_gene)
                    sbjct_length = alignment.length  # The length of matched gene
                    # print(sbjct_length)
                    sbjct_start = hsp.sbjct_start
                    sbjct_end = hsp.sbjct_end
                    gaps = hsp.gaps  # gaps of alignment
                    query_string = str(hsp.query)  # Get the query string
                    sbjct_string = str(hsp.sbjct)
                    identities_length = hsp.identities  # Number of indentity bases
                    # contig_name = query.replace(">", "")
                    query_start = hsp.query_start
                    query_end = hsp.query_end
                    # length of query sequence
                    query_length = len(query_string)

                    # calculate identities
                    perc_ident = (int(identities_length)
                                  / float(query_length) * 100)
                    IDENTITY = "%.2f" % perc_ident
                    # print("Identities: %s " % perc_ident)

                    # coverage = ((int(query_length) - int(gaps))
                    #             / float(sbjct_length))
                    # print(coverage)

                    perc_coverage = (((int(query_length) - int(gaps))
                                      / float(sbjct_length)) * 100)
                    COVERAGE = "%.2f" % perc_coverage

                    # print("Coverage: %s " % perc_coverage)

                    # cal_score is later used to select the best hit
                    cal_score = perc_ident * perc_coverage

                    # Calculate if the hit is on minus strand
                    if sbjct_start > sbjct_end:
                        temp = sbjct_start
                        sbjct_start = sbjct_end
                        sbjct_end = temp
                        strand = 1
                        query_string = str(
                            Seq(str(query_string)).reverse_complement())
                        sbjct_string = str(
                            Seq(str(sbjct_string)).reverse_complement())

                    if strand == 0:
                        strand_direction = '+'
                    else:
                        strand_direction = '-'

                    if (perc_coverage >= self.mincov) and (perc_ident >= self.minid):
                        loop_check += 1
                        hit_id = "%s:%s_%s:%s" % (
                            query_name, query_start, query_end, target_gene)
                        # print(hit_id)
                        # hit_id = query_name
                        # print(hit_id)
                        best_result = {
                            'FILE': os.path.basename(self.inputfile),
                            'SEQUENCE': query_name,
                            'GENE': gene,
                            'START': query_start,
                            'END': query_end,
                            'SBJSTART': sbjct_start,
                            'SBJEND': sbjct_end,
                            'STRAND': strand_direction,
                            # 'COVERAGE':
                            'GAPS': gaps,
                            "%COVERAGE": COVERAGE,
                            "%IDENTITY": IDENTITY,
                            # 'DATABASE':
                            'ACCESSION': accession,
                            'CLASSES': classes,
                            'QUERY_SEQ': query_string,
                            'SBJCT_SEQ': sbjct_string,
                            'cal_score': cal_score,
                            'remove': 0
                            # 'PRODUCT': target_gene,
                            # 'RESISTANCE': target_gene
                        }
                        # print(best_result)

                        # solve local variable referenced before assignment
                        if best_result:
                            save = 1

                            if hsp_results:
                                tmp_results = hsp_results
                                save, hsp_results = Blaster.filter_results(
                                    save, best_result, tmp_results)

                    if save == 1:
                        hsp_results[hit_id] = best_result
        # close file handler, then remove temp file
        result_handler.close()
        os.remove(self.temp_output)
        # print(self.inputfile)
        if loop_check == 0:
            df = pd.DataFrame(columns=['FILE', 'SEQUENCE', 'GENE', 'START', 'END', 'SBJSTART',
                                       'SBJEND', 'STRAND', 'GAPS', '%COVERAGE', '%IDENTITY', 'ACCESSION', 'CLASSES'])
        else:
            df = Blaster.resultdict2df(hsp_results)
        # print(hsp_results)
        return df, hsp_results

    def mlst_blast(self):
        cline = [self.blast_type, '-query', self.inputfile, '-db', self.database, '-dust', 'no', '-ungapped',
                 '-evalue', '1E-20', '-out', self.temp_output,
                 '-outfmt', '6 sseqid slen length nident', '-perc_identity', str(
                     self.minid), '-max_target_seqs', '1000000',
                 '-num_threads', str(self.threads)]

        # print(cline)

        # Run the command using subprocess
        cline_result = subprocess.run(
            cline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Capture the output and error
        stdout = cline_result.stdout
        stderr = cline_result.stderr

        # Print or handle the output and error as needed
        # print(stdout)
        if stderr:
            print(f"Error: {stderr}")

        df = pd.read_csv(self.temp_output, sep='\t', names=[
            'sseqid', 'slen', 'length', 'nident'])
        # print(df)

        result = {}
        for i, row in df.iterrows():
            gene, num = re.match(
                '^(\w+)[_-](\d+)', row['sseqid']).group(1, 2)
            # print(gene)
            num = int(num)
            hlen = row['slen']
            alen = row['length']
            nident = row['nident']
            if nident * 100 / hlen >= self.mincov:
                # if sch not in result.keys():  # check if sch is the key of result
                #     result[sch] = {}
                # resolve the bug that could not get exactly matched allele
                if hlen == alen & nident == hlen:  # exact match
                    if gene in result.keys():

                        if not re.search(r'[~\?]', str(result[gene])):
                            old_num = int(result[gene])
                            if num < old_num:
                                # print(f'{num}\t{old_num}')
                                result[gene] = num
                                print(
                                    f'Found additional allele match, replace {gene}:{old_num} -> {num}')
                            else:
                                print(
                                    f'Found additional allele match, but the allele number {num} is greater or equal to stored one {gene}:{old_num}, skip...')
                        else:  # replace not perfect match
                            result[gene] = num
                    else:
                        result[gene] = num
                # new allele
                elif (alen == hlen) & (nident != hlen):
                    # print('xx')
                    if gene not in result.keys():
                        # print('xxx')
                        result[gene] = f'~{num}'
                    else:
                        next
                    # result[sch] = mlst
                elif (alen != hlen) & (nident == hlen):  # partial match
                    if gene not in result.keys():
                        result[gene] = f'{num}?'
                else:
                    next
        # remove temp blastn output file
        os.remove(self.temp_output)
        return result

    @ staticmethod
    def filter_results(save, best_result, tmp_results):
        """
        remove the best hsp with coverage lt mincov
        参考bn的耐药基因过滤
        """

        new_query_name = best_result['SEQUENCE']
        new_query_start = best_result['START']
        new_query_end = best_result['END']
        new_sbjct_start = best_result['SBJSTART']
        new_sbjct_end = best_result['SBJEND']
        coverage = best_result['%COVERAGE']
        new_cal_score = best_result['cal_score']
        new_gene = best_result["GENE"]
        # print(new_gene)
        keys = list(tmp_results.keys())

        for hit in keys:
            remove_old = 0
            hit_data = tmp_results[hit]
            old_query_name = hit_data['SEQUENCE']
            if new_query_name == old_query_name:
                old_query_start = hit_data['START']
                old_query_end = hit_data['END']
                old_sbjct_start = hit_data['SBJSTART']
                old_sbjct_end = hit_data['SBJEND']
                old_cal_score = hit_data['cal_score']
                old_gene = hit_data['GENE']
                # print(old_gene)
                hit_union_length = (max(old_query_end, new_query_end)
                                    - min(old_query_start, new_query_start))
                hit_lengths_sum = ((old_query_end - old_query_start)
                                   + (new_query_end - new_query_start))
                overlap_len = (hit_lengths_sum - hit_union_length)

                if overlap_len <= 0:  # two genes without overlap, save all of them
                    continue
                # solve bug
                # else:  # tow genes with overlap
                #     if (old_query_start == new_query_start) and (old_query_end == new_query_end):
                #         if new_gene == old_gene:
                #             if new_cal_score > old_cal_score:
                #                 remove_old = 1
                #             elif new_cal_score == old_cal_score:
                #                 save = 1
                #             else:
                #                 save = 0
                #         else:
                #             save = 1
                #     elif (old_query_start != new_query_start) or (old_query_end != new_query_end):
                #         if new_gene == old_gene:
                #             if new_cal_score > old_cal_score:
                #                 remove_old = 1
                #             elif new_cal_score == old_cal_score:
                #                 save = 1
                #             else:
                #                 save = 0
                #         else:
                #             save = 1
                #     else:
                #         pass
                else:  # two genes with overlap
                    if (old_query_start == new_query_start) and (old_query_end == new_query_end):
                        if new_cal_score > old_cal_score:
                            remove_old = 1
                        elif new_cal_score == old_cal_score:
                            if new_gene == old_gene:
                                save = 0
                            else:
                                save = 1
                        else:
                            save = 0
                    elif (old_query_start != new_query_start) or (old_query_end != new_query_end):
                        if new_cal_score > old_cal_score:
                            remove_old = 1
                        elif new_cal_score == old_cal_score:
                            save = 1
                        else:
                            save = 0
                    else:
                        pass
            if remove_old == 1:
                del tmp_results[hit]
        return save, tmp_results

    @staticmethod
    def resultdict2df(result_dict):
        df_final = pd.DataFrame()
        col_dict = {'FILE': '',
                    'SEQUENCE': '',
                    'GENE': '',
                    'START': '',
                    'END': '',
                    'SBJSTART': '',
                    'SBJEND': '',
                    'STRAND': '',
                    'GAPS': '',
                    "%COVERAGE": '',
                    "%IDENTITY": '',
                    'ACCESSION': '',
                    'CLASSES': '',
                    'QUERY_SEQ': '',
                    'SBJCT_SEQ': '',
                    'cal_score': '',
                    'remove': ''}
        if len(result_dict.keys()) == 0:
            df_final = pd.DataFrame.from_dict(col_dict, orient='index')
        else:
            for key in result_dict.keys():
                hit_data = result_dict[key]
                df_tmp = pd.DataFrame.from_dict(hit_data, orient='index')
                df_final = pd.concat([df_final, df_tmp], axis=1)
        df_result = df_final.T
        df_result = df_result.drop(
            labels=['QUERY_SEQ', 'SBJCT_SEQ', 'cal_score', 'remove'], axis=1)
        return df_result

    @staticmethod
    def makeblastdb(file, name, db_type='nucl'):

        # cline = NcbimakeblastdbCommandline(
            # dbtype="nucl", out=name, input_file=file)
        # replace NcbimakeblastdbCommandline with makeblastdb command
        command = ['makeblastdb', '-hash_index', '-dbtype',
                   str(db_type), '-out', name, '-in', file]
        # print(command)
        print(f"Making {name} database...")
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # stdout, stderr = cline()
        # Capture the output and error
        stdout = result.stdout
        stderr = result.stderr
        # Print or handle the output and error as needed
        print(stdout)
        if stderr:
            print(f"Error: {stderr}")
        print('Finish')

    @staticmethod
    def get_arg_seq(file_base, result_dict, out_path):
        """
        save gene sequence
        """
        nucl_records = []
        prot_records = []
        prot_file = file_base + 'ARGs_prot.fasta'
        nucl_file = file_base + 'ARGs_nucl.fasta'
        prot_path = os.path.join(out_path, prot_file)
        nucl_path = os.path.join(out_path, nucl_file)
        if len(result_dict.keys()) == 0:
            print(f'No ARGs were found in {file_base}...')
        else:
            for key in result_dict.keys():
                hit_data = result_dict[key]
                # file = os.path.splitext(str(hit_data['FILE']))[0]
                # outfile = os.path.join(
                # out_path, file + str('_ARGs_nucl.fasta'))
                nucl_sequence = Seq(str(hit_data['QUERY_SEQ']))
                trim = len(nucl_sequence) % 3
                if trim != 0:
                    nucl_sequence = nucl_sequence + Seq('N' * (3 - trim))
                prot_sequence = nucl_sequence.replace('-', 'N').translate(
                    table=11, to_stop=True, gap='-')

                id = str(hit_data['SEQUENCE'] +
                         '_' + hit_data['GENE']) + str('_' + hit_data['ACCESSION'])
                name = str(hit_data['ACCESSION'])

                nucl_record = SeqRecord(nucl_sequence,
                                        id=id,
                                        name=name,
                                        description='')
                nucl_records.append(nucl_record)

                prot_record = SeqRecord(prot_sequence,
                                        id=id,
                                        name=name,
                                        description='')
                prot_records.append(prot_record)

            SeqIO.write(nucl_records, nucl_path, 'fasta')
            SeqIO.write(prot_records, prot_path, 'fasta')

    @staticmethod
    def is_fasta(file):
        """
        chcek if the input file is fasta format
        """
        try:
            with open(file, "r") as handle:
                fasta = SeqIO.parse(handle, "fasta")
                # False when `fasta` is empty, i.e. wasn't a FASTA file
                return any(fasta)
        except:
            print(f'The input file {file} is not a valid fasta file.')
            return False
