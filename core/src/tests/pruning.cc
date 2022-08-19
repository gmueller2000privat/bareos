/*
   BAREOS® - Backup Archiving REcovery Open Sourced

   Copyright (C) 2022-2022 Bareos GmbH & Co. KG

   This program is Free Software; you can redistribute it and/or
   modify it under the terms of version three of the GNU Affero General Public
   License as published by the Free Software Foundation and included
   in the file LICENSE.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
   02110-1301, USA.
*/

#include "testing_dir_common.h"

#include "include/jcr.h"
#include "dird/job.h"
#include "dird/ua_prune.h"

TEST(Pruning, ExcludeRunningJobsFromList)
{
  std::string path_to_config
      = std::string(RELATIVE_PROJECT_SOURCE_DIR "/configs/pruning/");
  PConfigParser director_config(DirectorPrepareResources(path_to_config));
  if (!director_config) { return; }

  JobControlRecord* jcr1 = directordaemon::NewDirectorJcr();
  jcr1->JobId = 1;
  JobControlRecord* jcr2 = directordaemon::NewDirectorJcr();
  jcr2->JobId = 2;
  JobControlRecord* jcr3 = directordaemon::NewDirectorJcr();
  jcr3->JobId = 3;

  std::vector<JobId_t> pruninglist{1, 2, 3, 4, 5};
  int NumJobsToBePruned
      = directordaemon::ExcludeRunningJobsFromList(pruninglist);

  EXPECT_EQ(NumJobsToBePruned, 2);
  EXPECT_EQ(pruninglist[0], 4);
  EXPECT_EQ(pruninglist[1], 5);
}
